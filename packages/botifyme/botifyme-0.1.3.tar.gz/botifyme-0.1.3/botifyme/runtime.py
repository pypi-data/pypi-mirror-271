import os
import json
from typing import Callable, List
from botifyme.config import (
    AgentInstanceRegistry,
    get_tool,
    get_function_details,
    tool_registry,
    workflow_registry,
    WorkflowConfig,
    Agent,
)
import importlib.util


def list_workflows() -> List[WorkflowConfig]:
    return list(workflow_registry.values())


def list_agents() -> List[str]:

    for agent in AgentInstanceRegistry.list_instances():
        print("Instance", agent)

    return []


def get_workflow(name: str) -> dict:

    workflow = workflow_registry.get(name)
    if workflow:
        _workflow = workflow.model_dump(
            exclude={"func"}, exclude_none=True, exclude_defaults=True
        )
        return _workflow

    # _agents: List["Agent"] = []
    # if workflow and len(workflow.agents) > 0:
    #     for agent in workflow.agents:
    #         _agent = AgentInstanceRegistry.instances.get(str(agent))
    #         if _agent:
    #             _agents.append(_agent)

    #     __workflow = workflow.model_dump(exclude={"agents", "func"})
    #     __workflow["agents"] = {}

    #     for agent in _agents:
    #         __agent = agent.model_dump(exclude={"tools"})
    #         __agent["tools"] = {}
    #         for tool_name in agent.tools:
    #             tool = get_tool(tool_name)
    #             __agent["tools"][tool_name] = tool.model_dump(exclude={"func"})
    #         __workflow["agents"][agent.name] = __agent

    #     return __workflow

    return {}


def load_modules_from_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            module_name = filename[:-3]  # Remove the '.py' from filename
            file_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)


def write_config_file(config, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(config, indent=2))


def generate_config():
    """
    Generate workflow configuration files in the '.botifyme' directory based on available workflows.

    This function fetches the current working directory, creates a '.botifyme' directory if it doesn't exist,
    clears existing workflow files, and writes new workflow configurations in JSON format for each available workflow.
    """
    working_directory = os.getcwd()
    load_modules_from_directory(working_directory)
    botifyme_dir = os.path.join(working_directory, ".botifyme")

    # Create the '.botifyme' directory if it doesn't exist
    if not os.path.exists(botifyme_dir):
        os.makedirs(botifyme_dir)

    botifyme_config_dir = os.path.join(botifyme_dir, "config")

    # Create or clear the 'workflows' directory
    if not os.path.exists(botifyme_config_dir):
        os.makedirs(botifyme_config_dir)
    else:
        for file in os.listdir(botifyme_config_dir):
            os.remove(os.path.join(botifyme_config_dir, file))

    # Save tool configuration to `tools.json`
    tools_config = []
    for _, tool in tool_registry.items():
        tool_config = tool.model_dump(
            exclude={"func"}, exclude_unset=True, exclude_none=True
        )
        tools_config.append(tool_config)
    write_config_file(tools_config, os.path.join(botifyme_config_dir, "tools.json"))

    # Save agent configuration to `agents.json`
    agents_config = []
    for _, agent in AgentInstanceRegistry.list_instances().items():
        agent_config = agent.model_dump(exclude_unset=True, exclude_none=True)
        agents_config.append(agent_config)
    write_config_file(agents_config, os.path.join(botifyme_config_dir, "agents.json"))

    workflows = list_workflows()
    workflows_config = []
    for workflow in workflows:
        workflow_config = get_workflow(workflow.name)
        workflows_config.append(workflow_config)
    write_config_file(
        workflows_config, os.path.join(botifyme_config_dir, "workflows.json")
    )
