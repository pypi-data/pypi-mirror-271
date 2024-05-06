# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import os
import re
from os import PathLike
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

from jinja2 import Template

from promptflow._constants import AZURE_WORKSPACE_REGEX_FORMAT
from promptflow._utils.flow_utils import is_flex_flow, resolve_flow_path, resolve_python_entry_file
from promptflow._utils.logger_utils import LoggerFactory
from promptflow._utils.utils import _match_reference
from promptflow._utils.yaml_utils import load_yaml
from promptflow.core._errors import InvalidSampleError, MalformedConnectionProviderConfig, MissingRequiredPackage
from promptflow.exceptions import UserErrorException

logger = LoggerFactory.get_logger(name=__name__)


def render_jinja_template_content(template_content, *, trim_blocks=True, keep_trailing_newline=True, **kwargs):
    template = Template(template_content, trim_blocks=trim_blocks, keep_trailing_newline=keep_trailing_newline)
    return template.render(**kwargs)


def init_executable(*, flow_dag: dict = None, flow_path: Path = None, working_dir: Path = None):
    if flow_dag and flow_path:
        raise ValueError("flow_dag and flow_path cannot be both provided.")
    if not flow_dag and not flow_path:
        raise ValueError("flow_dag or flow_path must be provided.")
    if flow_dag and not working_dir:
        raise ValueError("working_dir must be provided when flow_dag is provided.")

    if flow_path:
        flow_dir, flow_filename = resolve_flow_path(flow_path)
        flow_dag = load_yaml(flow_dir / flow_filename)
        if not working_dir:
            working_dir = flow_dir

    from promptflow.contracts.flow import FlexFlow as ExecutableEagerFlow
    from promptflow.contracts.flow import Flow as ExecutableFlow

    if is_flex_flow(yaml_dict=flow_dag):

        entry = flow_dag.get("entry")
        entry_file = resolve_python_entry_file(entry=entry, working_dir=working_dir)

        from promptflow._core.entry_meta_generator import generate_flow_meta

        meta_dict = generate_flow_meta(
            flow_directory=working_dir,
            source_path=entry_file,
            data=flow_dag,
        )
        return ExecutableEagerFlow.deserialize(meta_dict)

    # for DAG flow, use data to init executable to improve performance
    return ExecutableFlow._from_dict(flow_dag=flow_dag, working_dir=working_dir)


# !!! Attention!!!: Please make sure you have contact with PRS team before changing the interface.
# They are using FlowExecutor.update_environment_variables_with_connections(connections)
def update_environment_variables_with_connections(built_connections):
    """The function will result env var value ${my_connection.key} to the real connection keys."""
    return update_dict_value_with_connections(built_connections, os.environ)


def override_connection_config_with_environment_variable(connections: Dict[str, dict]):
    """
    The function will use relevant environment variable to override connection configurations. For instance, if there
    is a custom connection named 'custom_connection' with a configuration key called 'chat_deployment_name,' the
    function will attempt to retrieve 'chat_deployment_name' from the environment variable
    'CUSTOM_CONNECTION_CHAT_DEPLOYMENT_NAME' by default. If the environment variable is not set, it will use the
    original value as a fallback.
    """
    for connection_name, connection in connections.items():
        values = connection.get("value", {})
        for key, val in values.items():
            connection_name = connection_name.replace(" ", "_")
            env_name = f"{connection_name}_{key}".upper()
            if env_name not in os.environ:
                continue
            values[key] = os.environ[env_name]
            logger.info(f"Connection {connection_name}'s {key} is overridden with environment variable {env_name}")
    return connections


def resolve_connections_environment_variable_reference(connections: Dict[str, dict]):
    """The function will resolve connection secrets env var reference like api_key: ${env:KEY}"""
    for connection in connections.values():
        values = connection.get("value", {})
        for key, val in values.items():
            if not _match_env_reference(val):
                continue
            env_name = _match_env_reference(val)
            if env_name not in os.environ:
                raise UserErrorException(f"Environment variable {env_name} is not found.")
            values[key] = os.environ[env_name]
    return connections


def _match_env_reference(val: str):
    try:
        val = val.strip()
        m = re.match(r"^\$\{env:(.+)}$", val)
        if not m:
            return None
        name = m.groups()[0]
        return name
    except Exception:
        # for exceptions when val is not a string, return
        return None


def get_used_connection_names_from_environment_variables():
    """The function will get all potential related connection names from current environment variables.
    for example, if part of env var is
    {
      "ENV_VAR_1": "${my_connection.key}",
      "ENV_VAR_2": "${my_connection.key2}",
      "ENV_VAR_3": "${my_connection2.key}",
    }
    The function will return {"my_connection", "my_connection2"}.
    """
    return get_used_connection_names_from_dict(os.environ)


def update_dict_value_with_connections(built_connections, connection_dict: dict):
    for key, val in connection_dict.items():
        connection_name, connection_key = _match_reference(val)
        if connection_name is None:
            continue
        if connection_name not in built_connections:
            continue
        if connection_key not in built_connections[connection_name]["value"]:
            continue
        connection_dict[key] = built_connections[connection_name]["value"][connection_key]


def get_used_connection_names_from_dict(connection_dict: dict):
    connection_names = set()
    for key, val in connection_dict.items():
        connection_name, _ = _match_reference(val)
        if connection_name:
            connection_names.add(connection_name)

    return connection_names


def extract_workspace(provider_config) -> Tuple[str, str, str]:
    match = re.match(AZURE_WORKSPACE_REGEX_FORMAT, provider_config)
    if not match or len(match.groups()) != 5:
        raise MalformedConnectionProviderConfig(provider_config=provider_config)
    subscription_id = match.group(1)
    resource_group = match.group(3)
    workspace_name = match.group(5)
    return subscription_id, resource_group, workspace_name


def get_workspace_from_resource_id(resource_id: str, credential, pkg_name: Optional[str] = None):
    # check azure extension first
    try:
        from azure.ai.ml import MLClient
    except ImportError as e:
        if pkg_name is not None:
            error_msg = f"Please install '{pkg_name}' to use Azure related features."
        else:
            error_msg = (
                "Please install Azure extension (e.g. `pip install promptflow-azure`) to use Azure related features."
            )
        raise MissingRequiredPackage(message=error_msg) from e
    # extract workspace triad and get from Azure
    subscription_id, resource_group_name, workspace_name = extract_workspace(resource_id)
    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name,
    )
    return ml_client.workspaces.get(name=workspace_name)


def load_inputs_from_sample(sample: Union[dict, str, PathLike]):
    if not sample:
        return {}
    elif isinstance(sample, dict):
        return sample
    elif isinstance(sample, (str, Path)) and str(sample).endswith(".json"):
        if str(sample).startswith("file:"):
            sample = sample[len("file:") :]
        if not Path(sample).exists():
            raise InvalidSampleError(f"Cannot find sample file {sample}.")
        with open(sample, "r") as f:
            return json.load(f)
    else:
        raise InvalidSampleError("Only dict and json file are supported as sample in prompty.")
