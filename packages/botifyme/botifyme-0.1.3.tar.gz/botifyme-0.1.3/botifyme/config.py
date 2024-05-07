import functools
from loguru import logger
import inspect
from typing import Any, Dict, Union, Callable, ParamSpec, TypeVar, List, Optional
from pydantic import BaseModel
from docstring_parser import parse
from slugify import slugify

P = ParamSpec("P")
R = TypeVar("R", bound=Callable[..., Any])

workflow_registry: Dict[str, "WorkflowConfig"] = {}
task_registry: Dict[str, Any] = {}
tool_registry: Dict[str, "Tool"] = {}


class AgentInstanceRegistry:
    instances: Dict[str, "Agent"] = {}

    @classmethod
    def add_instance(cls, instance):
        if instance.name not in cls.instances:
            cls.instances[instance.name] = instance

    @classmethod
    def list_instances(cls) -> Dict[str, "Agent"]:
        return cls.instances


class Workflow(BaseModel):
    name: str
    description: str
    agents: List[Union[BaseModel, str]] = []


class LLM(BaseModel):
    name: str
    provider: str
    slug: str
    api_key: Optional[str] = None
    top_p: Optional[float] = None
    temperature: Optional[float] = None

    class Config:
        """ """

        json_schema_extra = {
            "example": {
                "name": "GPT-3",
                "provider": "OpenAI",
                "slug": "gpt-3",
                "api_key": "your-api-key",
                "top_p": 0.9,
                "temperature": 0.7,
            }
        }


class Environment(BaseModel):
    name: str
    slug: str
    language_with_version: str
    docker_image: str
    packages: List[str]

    class Config:
        """ """

        json_schema_extra = {
            "example": {
                "name": "Python Environment",
                "slug": "python-env",
                "language_with_version": "Python 3.8",
                "docker_image": "python:3.8-slim",
                "packages": ["numpy", "pandas"],
            }
        }


class Agent(BaseModel):
    """
    Base class for all agents.
    """

    def __init__(self, **data: Any):
        super().__init__(**data)
        AgentInstanceRegistry.add_instance(self)

    name: str
    description: Optional[str] = None
    slug: str = ""
    system_prompt: str = ""
    instructions: str = ""
    tools: List[str] = []
    llm: LLM | None = None
    environment: Environment | None = None
    input_params: Union[Dict[str, Any], BaseModel, str] = ""
    response_type: Union[Dict[str, Any], BaseModel, str] = ""

    def __post_init_post_parse__(self):
        if self.slug == "" and self.name:
            self.slug = slugify(self.name)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Code Assistant",
                "description": "A versatile coding agent",
                "slug": "code-assistant",
                "system_prompt": "Please write a Python script for:",
                "instructions": "Ensure to handle exceptions properly.",
                "tools": ["browser", "python"],
                "llm": {
                    "name": "GPT-3",
                    "provider": "OpenAI",
                    "slug": "gpt-3",
                    "api_key": "your-api-key",
                    "top_p": 0.9,
                    "temperature": 0.7,
                },
                "environment": {
                    "name": "Python Environment",
                    "slug": "python-env",
                    "language_with_version": "Python 3.8",
                    "docker_image": "python:3.8-slim",
                    "packages": ["numpy", "pandas"],
                },
            }
        }
        frozen = True


class Param(BaseModel):
    """
    Represents a parameter.

    Attributes:
        name (str): The name of the parameter.
        description (str): The description of the parameter.
        data_type (str): The data type of the parameter.
        default_value (Any): The default value of the parameter. Defaults to None.
        required (bool): Whether the parameter is required. Defaults to True.
    """

    name: str
    description: str
    data_type: str
    default_value: Any = None
    required: bool

    class Config:
        """Pydantic configuration."""

        frozen = True


class Tool(BaseModel):
    """
    Base class for all tools.

    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
    """

    name: str
    description: str
    slug: str
    func: Callable[..., Any]
    input_params: List[Param]
    output_params: List[Param]

    class Config:
        """Pydantic configuration."""

        frozen = True


def get_json_datatype_from_python_type(python_type: str) -> str:
    if python_type == "str":
        return "string"
    if python_type == "int":
        return "number"
    if python_type == "float":
        return "number"
    if python_type == "bool":
        return "boolean"
    if python_type == "list":
        return "array"
    return "string"


def get_function_details(func):
    """Extract details from a function, including its name, description, and parameter info."""
    docstring = inspect.getdoc(func)
    parsed_docstring = parse(docstring)

    sig = inspect.signature(func)

    input_params: List[Param] = []
    for param in sig.parameters.values():
        param_name = param.name
        if param_name == "self":
            continue

        param_doc = next(
            (p for p in parsed_docstring.params if p.arg_name == param_name), None
        )

        param_type = (
            str(param_doc.type_name)
            if param_doc and param.annotation != inspect.Parameter.empty
            else "string"
        )

        # Determine if parameter is optional based on its default value
        is_optional = param.default != inspect.Parameter.empty
        param_desc = param_doc.description if param_doc else ""

        _param = Param(
            name=param_name,
            description=param_desc,
            data_type=get_json_datatype_from_python_type(param_type),
            default_value=(
                param.default if param.default != inspect.Parameter.empty else None
            ),
            required=not is_optional,
        )

        input_params.append(_param)

    # Parse output paramters from return type
    output_params: List[Param] = []
    return_annotation = sig.return_annotation

    if return_annotation != inspect.Signature.empty:
        if issubclass(return_annotation, str):
            _param = Param(
                name="output",
                description="The output of the function.",
                data_type="string",
                default_value="",
                required=True,
            )
            output_params.append(_param)

        elif issubclass(return_annotation, BaseModel):
            for field_name, model_field in return_annotation.model_fields.items():
                _param = Param(
                    name=field_name,
                    description="",
                    data_type=get_json_datatype_from_python_type(
                        model_field.annotation
                    ),
                    default_value=model_field.default,
                    required=model_field.is_required(),
                )
                output_params.append(_param)

    func_details = {}
    func_details["name"] = func.__name__
    func_details["description"] = parsed_docstring.short_description
    func_details["input_params"] = input_params
    func_details["output_params"] = output_params

    return func_details


def tool(name: str, description: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Creates a decorator that logs the call details of the function it decorates,
    and stores the function in a global registry under the provided name.

    Args:
    name (str): The name of the tool.
    description (str): A brief description of what the tool does.

    Returns:
    Callable: A decorator that enhances functions with logging and registration capabilities.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:

        func_details = get_function_details(func)
        func_name = func_details["name"]
        slug = slugify(func_name)

        config = Tool(
            name=func_name,
            slug=slug,
            description=str(func_details["description"]),
            func=func,
            input_params=func_details.get("input_params", {}),
            output_params=func_details.get("output_params", {}),
        )

        tool_registry[slug] = config

        @functools.wraps(func)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            result = func(*args, **kwargs)
            return result

        # pylint: disable=protected-access
        wrapped.__config = config  # type: ignore
        return wrapped

    return decorator


def get_tool(name: str) -> "Tool":
    """Get the tool with the given name."""
    if name not in tool_registry:
        raise ValueError(f"Tool {name} not found.")

    return tool_registry[name]


def get_tools() -> Dict[str, "Tool"]:
    """Get all registered tools."""
    return tool_registry


class WorkflowConfig(BaseModel):
    """
    Represents the configuration of a workflow.

    Attributes:
        id (str): The unique identifier of the workflow.
        slug (str): The slug of the workflow.
        func (Callable[..., Any]): The function to be executed by the workflow.
        name (str): The name of the workflow.
        description (str): The description of the workflow.
    """

    slug: str
    func: Callable[..., Any]
    name: str
    description: str
    agents: List[Union[BaseModel, str]] = []
    tasks: List[Union[BaseModel, str]] = []
    input_params: List[Param] = []
    output_params: List[Param] = []

    class Config:
        """Pydantic configuration."""

        frozen = True


class WorkflowRun(BaseModel):
    id: str
    status: str


def execute_workflow_async(slug: str, kwargs: Dict[str, Any]) -> WorkflowRun:

    return WorkflowRun(id=slug, status="success")


def execute_workflow(slug: str, *args, kwargs: Dict[str, Any], func) -> R:
    return func(**kwargs)


def workflow(
    name: str,
    description: str,
    agents: List[Union[BaseModel, str]] = [],
    tasks: List[Union[BaseModel, str]] = [],
) -> Callable[[Callable[P, R]], Callable[P, Union[R, WorkflowRun]]]:
    """
    Creates a decorator that logs the call details of the function it decorates,
    and stores the function in a global registry under the provided name.

    Args:
    name (str): The name of the workflow.
    description (str): A brief description of what the workflow does.

    Returns:
    Callable: A decorator that enhances functions with logging and registration capabilities.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, Union[R, WorkflowRun]]:

        func_details = get_function_details(func)
        config = WorkflowConfig(
            slug=name,
            func=func,
            name=name,
            description=description if description else func_details["description"],
            agents=agents,
            tasks=tasks,
            input_params=func_details.get("input_params", {}),
            output_params=func_details.get("output_params", {}),
        )
        workflow_registry[name] = config

        is_async_fn = inspect.iscoroutinefunction(func)

        @functools.wraps(func)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> Union[R, WorkflowRun]:
            logger.info(f"Calling {name}: {description}")
            if is_async_fn:
                return execute_workflow_async(slug=name, kwargs=kwargs)

            return execute_workflow(slug=name, kwargs=kwargs, func=func)

        # pylint: disable=protected-access
        wrapped.__config = config  # type: ignore
        return wrapped

    return decorator
