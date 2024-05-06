# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import abc
import re
from os import PathLike
from pathlib import Path
from typing import Any, Mapping, Union

from promptflow._constants import DEFAULT_ENCODING, LANGUAGE_KEY, PROMPTY_EXTENSION, FlowLanguage
from promptflow._utils.flow_utils import is_flex_flow, is_prompty_flow, resolve_flow_path
from promptflow._utils.yaml_utils import load_yaml_string
from promptflow.core._errors import MissingRequiredInputError
from promptflow.core._model_configuration import PromptyModelConfiguration
from promptflow.core._prompty_utils import (
    convert_model_configuration_to_connection,
    convert_prompt_template,
    format_llm_response,
    get_open_ai_client_by_connection,
    prepare_open_ai_request_params,
    send_request_to_llm,
    update_dict_recursively,
)
from promptflow.core._utils import load_inputs_from_sample
from promptflow.exceptions import UserErrorException
from promptflow.tracing import trace
from promptflow.tracing._experimental import enrich_prompt_template
from promptflow.tracing._trace import _traced


class AbstractFlowBase(abc.ABC):
    """Abstract class for all Flow entities in both core and devkit."""

    def __init__(self, *, data: dict, code: Path, path: Path, **kwargs):
        # yaml content if provided
        self._data = data
        # working directory of the flow
        self._code = Path(code).resolve()
        # flow file path, can be script file or flow definition YAML file
        self._path = Path(path).resolve()


class FlowBase(AbstractFlowBase):
    def __init__(self, *, data: dict, code: Path, path: Path, **kwargs):
        super().__init__(data=data, code=code, path=path, **kwargs)

    @property
    def code(self) -> Path:
        """Working directory of the flow."""
        return self._code

    @property
    def path(self) -> Path:
        """Flow file path. Can be script file or flow definition YAML file."""
        return self._path

    @classmethod
    def load(
        cls,
        source: Union[str, PathLike],
        **kwargs,
    ) -> "Flow":
        """
        Load flow from YAML file.

        :param source: The local yaml source of a flow. Must be a path to a local file.
            If the source is a path, it will be open and read.
            An exception is raised if the file does not exist.
        :type source: Union[PathLike, str]
        :return: A Flow object
        :rtype: Flow
        """
        flow_dir, flow_filename = resolve_flow_path(source)
        flow_path = flow_dir / flow_filename
        if is_prompty_flow(flow_path):
            return Prompty.load(source=flow_path, **kwargs)

        with open(flow_path, "r", encoding=DEFAULT_ENCODING) as f:
            flow_content = f.read()
            data = load_yaml_string(flow_content)
        flow_language = data.get(LANGUAGE_KEY, FlowLanguage.Python)
        if flow_language != FlowLanguage.Python:
            raise UserErrorException(
                message_format="Only python flows are allowed to be loaded with "
                "promptflow-core but got a {language} flow",
                language=flow_language,
            )

        return cls._create(code=flow_dir, path=flow_path, data=data)

    @classmethod
    def _create(cls, data, code, path, **kwargs):
        raise NotImplementedError()


class Flow(FlowBase):
    """A Flow in the context of PromptFlow is a sequence of steps that define a task.
    Each step in the flow could be a prompt that is sent to a language model, or simply a function task,
    and the output of one step can be used as the input to the next.
    Flows can be used to build complex applications with language models.

    Example:

    .. code-block:: python

        from promptflow.core import Flow
        flow = Flow.load(source="path/to/flow.yaml")
        result = flow(input_a=1, input_b=2)

    """

    def __call__(self, *args, **kwargs) -> Mapping[str, Any]:
        """Calling flow as a function, the inputs should be provided with key word arguments.
        Returns the output of the flow.
        The function call throws UserErrorException: if the flow is not valid or the inputs are not valid.
        SystemErrorException: if the flow execution failed due to unexpected executor error.

        :param args: positional arguments are not supported.
        :param kwargs: flow inputs with key word arguments.
        :return:
        """

        if args:
            raise UserErrorException("Flow can only be called with keyword arguments.")

        result = self.invoke(inputs=kwargs)
        return result.output

    def invoke(self, inputs: dict, connections: dict = None, **kwargs) -> "LineResult":
        """Invoke a flow and get a LineResult object."""
        # candidate parameters: connections, variant, overrides, streaming
        from promptflow._utils.logger_utils import LoggerFactory

        with LoggerFactory.disable_all_loggers():
            return self._invoke(inputs=inputs, connections=connections, **kwargs)

    def _invoke(self, inputs: dict, connections: dict = None, **kwargs) -> "LineResult":
        from promptflow.core._serving.flow_invoker import FlowInvoker

        if is_flex_flow(yaml_dict=self._data, working_dir=self.code):
            raise UserErrorException("Please call entry directly for flex flow.")

        invoker = FlowInvoker(
            flow=self,
            connections=connections,
            streaming=True,
        )
        result = invoker._invoke(
            data=inputs,
        )
        return result

    @classmethod
    def _create(cls, data, code, path, **kwargs):
        return cls(code=code, path=path, data=data, **kwargs)


class AsyncFlow(FlowBase):
    """Async flow is based on Flow, which is used to invoke flow in async mode.

    Example:

    .. code-block:: python

        from promptflow.core import class AsyncFlow
        flow = AsyncFlow.load(source="path/to/flow.yaml")
        result = await flow(input_a=1, input_b=2)

    """

    async def __call__(self, *args, **kwargs) -> Mapping[str, Any]:
        """Calling flow as a function in async, the inputs should be provided with key word arguments.
        Returns the output of the flow.
        The function call throws UserErrorException: if the flow is not valid or the inputs are not valid.
        SystemErrorException: if the flow execution failed due to unexpected executor error.

        :param args: positional arguments are not supported.
        :param kwargs: flow inputs with key word arguments.
        :return:
        """
        if args:
            raise UserErrorException("Flow can only be called with keyword arguments.")

        result = await self.invoke(inputs=kwargs)
        return result.output

    async def invoke(self, inputs: dict, *, connections: dict = None, **kwargs) -> "LineResult":
        """Invoke a flow and get a LineResult object."""

        from promptflow.core._serving.flow_invoker import AsyncFlowInvoker

        invoker = AsyncFlowInvoker(
            flow=self,
            connections=connections,
            streaming=True,
            flow_path=self.path,
            working_dir=self.code,
        )
        result = await invoker._invoke_async(
            data=inputs,
        )
        return result

    @classmethod
    def _create(cls, data, code, path, **kwargs):
        return cls(code=code, path=path, data=data, **kwargs)


class Prompty(FlowBase):
    """A prompty is a prompt with predefined metadata like inputs, and can be executed directly like a flow.
    A prompty is represented as a templated markdown file with a modified front matter.
    The front matter is a yaml file that contains meta fields like model configuration, inputs, etc..

    Prompty example:
    .. code-block::

        ---
        name: Hello Prompty
        description: A basic prompt
        model:
            api: chat
            configuration:
              type: azure_openai
              azure_deployment: gpt-35-turbo
              api_key="${env:AZURE_OPENAI_API_KEY}",
              api_version=${env:AZURE_OPENAI_API_VERSION}",
              azure_endpoint="${env:AZURE_OPENAI_ENDPOINT}",
            parameters:
              max_tokens: 128
              temperature: 0.2
        inputs:
          text:
            type: string
        ---
        system:
        Write a simple {{text}} program that displays the greeting message.

    Prompty as function example:

    .. code-block:: python

        from promptflow.core import Prompty
        prompty = Prompty.load(source="path/to/prompty.prompty")
        result = prompty(input_a=1, input_b=2)

        # Override model config with dict
        model_config = {
            "api": "chat",
            "configuration": {
                "type": "azure_openai",
                "azure_deployment": "gpt-35-turbo",
                "api_key": "${env:AZURE_OPENAI_API_KEY}",
                "api_version": "${env:AZURE_OPENAI_API_VERSION}",
                "azure_endpoint": "${env:AZURE_OPENAI_ENDPOINT}",
            },
            "parameters": {
                "max_token": 512
            }
        }
        prompty = Prompty.load(source="path/to/prompty.prompty", model=model_config)
        result = prompty(input_a=1, input_b=2)

        # Override model config with configuration
        from promptflow.core import AzureOpenAIModelConfiguration
        model_config = {
            "api": "chat",
            "configuration": AzureOpenAIModelConfiguration(
                azure_deployment="gpt-35-turbo",
                api_key="${env:AZURE_OPENAI_API_KEY}",
                api_version="${env:AZURE_OPENAI_API_VERSION}",
                azure_endpoint="${env:AZURE_OPENAI_ENDPOINT}",
            ),
            "parameters": {
                "max_token": 512
            }
        }
        prompty = Prompty.load(source="path/to/prompty.prompty", model=model_config)
        result = prompty(input_a=1, input_b=2)

        # Override model config with created connection
        from promptflow.core._model_configuration import AzureOpenAIModelConfiguration
        model_config = {
            "api": "chat",
            "configuration": AzureOpenAIModelConfiguration(
                connection="azure_open_ai_connection",
                azure_deployment="gpt-35-turbo",
            ),
            "parameters": {
                "max_token": 512
            }
        }
        prompty = Prompty.load(source="path/to/prompty.prompty", model=model_config)
        result = prompty(input_a=1, input_b=2)
    """

    def __init__(
        self,
        path: Union[str, PathLike],
        model: dict = None,
        **kwargs,
    ):
        # prompty file path
        path = Path(path)
        configs, self._template = self._parse_prompty(path)
        configs = update_dict_recursively(configs, kwargs)
        configs["model"] = update_dict_recursively(configs.get("model", {}), model or {})

        self._model = PromptyModelConfiguration(**configs["model"])
        self._inputs = configs.get("inputs", {})
        self._outputs = configs.get("outputs", {})
        self._name = configs.get("name", path.stem)
        self._sample = configs.get("sample", None)

        # TODO support more templating engine
        self._template_engine = configs.get("template", "jinja2")
        super().__init__(code=path.parent, path=path, data=configs, content_hash=None, **kwargs)

    @classmethod
    def _load(cls, path: Path, **kwargs):
        return cls(path=path, **kwargs)

    # region overrides
    @classmethod
    def load(
        cls,
        source: Union[str, PathLike],
        **kwargs,
    ) -> "Prompty":
        """
        Direct load non-dag flow from prompty file.

        :param source: The local prompt file. Must be a path to a local file.
            If the source is a path, it will be open and read.
            An exception is raised if the file does not exist.
        :type source: Union[PathLike, str]
        :return: A Prompty object
        :rtype: Prompty
        """
        source_path = Path(source)
        if not source_path.exists():
            raise UserErrorException(f"Source {source_path.absolute().as_posix()} does not exist")

        if source_path.suffix != PROMPTY_EXTENSION:
            raise UserErrorException("Source must be a file with .prompty extension.")
        return cls._load(path=source_path, **kwargs)

    @staticmethod
    def _parse_prompty(path):
        """ """
        with open(path, "r", encoding=DEFAULT_ENCODING) as f:
            prompty_content = f.read()
        pattern = r"-{3,}\n(.*)-{3,}\n(.*)"
        result = re.search(pattern, prompty_content, re.DOTALL)
        if not result:
            raise UserErrorException(
                "Illegal formatting of prompty. The prompt file is in markdown format and can be divided into two "
                "parts, the first part is in YAML format and contains connection and model information. The second "
                "part is the prompt template."
            )
        config_content, prompt_template = result.groups()
        configs = load_yaml_string(config_content)
        return configs, prompt_template

    def _validate_inputs(self, input_values):
        resolved_inputs = {}
        missing_inputs = []
        for input_name, value in self._inputs.items():
            if input_name not in input_values and "default" not in value:
                missing_inputs.append(input_name)
                continue
            resolved_inputs[input_name] = input_values.get(input_name, value.get("default", None))
        if missing_inputs:
            raise MissingRequiredInputError(f"Missing required inputs: {missing_inputs}")
        return resolved_inputs

    @trace
    def __call__(self, *args, **kwargs):
        """Calling flow as a function, the inputs should be provided with key word arguments.
        Returns the output of the prompty.
        The function call throws UserErrorException: if the flow is not valid or the inputs are not valid.
        SystemErrorException: if the flow execution failed due to unexpected executor error.

        :param args: positional arguments are not supported.
        :param kwargs: flow inputs with key word arguments.
        :return:
        """
        if args:
            raise UserErrorException("Prompty can only be called with keyword arguments.")
        inputs = kwargs
        if not inputs and self._sample:
            # Load inputs from sample
            inputs = load_inputs_from_sample(self._sample)
        enrich_prompt_template(self._template, variables=inputs)

        # 1. Get connection
        connection = convert_model_configuration_to_connection(self._model.configuration)

        # 2.deal with prompt
        inputs = self._validate_inputs(inputs)
        traced_convert_prompt_template = _traced(func=convert_prompt_template, args_to_ignore=["api"])
        template = traced_convert_prompt_template(self._template, inputs, self._model.api)

        # 3. prepare params
        params = prepare_open_ai_request_params(self._model, template, connection)

        # 4. send request to open ai
        api_client = get_open_ai_client_by_connection(connection=connection)

        response = send_request_to_llm(api_client, self._model.api, params)
        return format_llm_response(
            response=response,
            api=self._model.api,
            response_format=params.get("response_format", {}),
            is_first_choice=self._data.get("model", {}).get("response", None) != "all",
            streaming=params.get("stream", False),
            outputs=self._outputs,
        )


class AsyncPrompty(Prompty):
    """Async prompty is based on Prompty, which is used to invoke prompty in async mode.

    Simple Example:

    .. code-block:: python

        import asyncio
        from promptflow.core import AsyncPrompty
        prompty = AsyncPrompty.load(source="path/prompty.prompty")
        result = await prompty(input_a=1, input_b=2)

    """

    @trace
    async def __call__(self, *args, **kwargs) -> Mapping[str, Any]:
        """Calling prompty as a function in async, the inputs should be provided with key word arguments.
        Returns the output of the prompty.
        The function call throws UserErrorException: if the flow is not valid or the inputs are not valid.
        SystemErrorException: if the flow execution failed due to unexpected executor error.

        :param args: positional arguments are not supported.
        :param kwargs: flow inputs with key word arguments.
        :return:
        """
        if args:
            raise UserErrorException("Prompty can only be called with keyword arguments.")
        inputs = kwargs
        if not inputs and self._sample:
            # Load inputs from sample
            inputs = load_inputs_from_sample(self._sample)
        enrich_prompt_template(self._template, variables=inputs)

        # 1. Get connection
        connection = convert_model_configuration_to_connection(self._model.configuration)

        # 2.deal with prompt
        inputs = self._validate_inputs(inputs)
        traced_convert_prompt_template = _traced(func=convert_prompt_template, args_to_ignore=["api"])
        template = traced_convert_prompt_template(self._template, inputs, self._model.api)

        # 3. prepare params
        params = prepare_open_ai_request_params(self._model, template, connection)

        # 4. send request to open ai
        api_client = get_open_ai_client_by_connection(connection=connection, is_async=True)

        response = await send_request_to_llm(api_client, self._model.api, params)
        return format_llm_response(
            response=response,
            api=self._model.api,
            response_format=params.get("response_format", {}),
            is_first_choice=self._data.get("model", {}).get("response", None) != "all",
            streaming=params.get("stream", False),
            outputs=self._outputs,
        )
