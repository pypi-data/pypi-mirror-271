import functools
from loguru import logger
from typing import Callable, ParamSpec, Any, Optional, Dict
from pydantic import BaseModel


class WorkflowConfig(BaseModel):
    id: str
    slug: str
    func: Callable[..., Any]
    name: str
    description: str
    version: str
    language: str = "python"

    class Config:
        frozen = True


class WorkflowRun(BaseModel):
    id: str
    config: WorkflowConfig

    def run(self, *args, **kwargs):
        self.config.func(*args, **kwargs)


# class Workflow:
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description
#         self.steps = []

#     def register(self, func):
#         """Decorator to register a new workflow step."""

#         def wrapper():
#             print(f"Executing {func.__name__}...")
#             print(self.name)
#             print(self.description)
#             return func()

#         self.steps.append(wrapper)
#         return wrapper

#     def run(self):
#         """Execute all the steps registered to this workflow."""
#         for step in self.steps:
#             step()


P = ParamSpec("P")


# def execute(
#     slug: str,
#     param_values: Optional[Dict[str, Any]] = None,
#     allow_cached_max_age: Optional[int] = None,
# ) -> WorkflowRun:
#     """Execute a workflow run."""
#     logger.info(f"Executing workflow {slug} with params {param_values}")
#     print(param_values)

#     workflow_run = WorkflowRun(id="123", config=param_values["__workflow_config"])

#     from inspect import signature

#     _params = signature(workflow_run.config.func).parameters
#     _param_values = {k: v for k, v in param_values.items() if k in _params}
#     workflow_run.run(**_param_values)

#     return workflow_run


# def workflow(
#     name, description, agents
# ) -> Callable[[Callable[P, Any]], Callable[P, WorkflowRun]]:
#     """Decorator factory that creates a new workflow."""

#     def decorator(func: Callable[P, Any]) -> Callable[P, WorkflowRun]:

#         workflow_config = WorkflowConfig(
#             id="asdf", slug="adsf", func=func, name=name, description=description
#         )

#         @functools.wraps(func)
#         def wrapped(*args: P.args, **kwargs: P.kwargs) -> WorkflowRun:
#             kwargs.update(zip(func.__code__.co_varnames, args))
#             kwargs["__workflow_config"] = workflow_config
#             return execute(workflow_config.slug, kwargs)

#         return wrapped

#     return decorator


# def task(name: Optional[str] = None, description: Optional[str] = None):
#     """Decorator factory that creates a new task."""

#     def decorator(func: Callable[P, Any]) -> Callable[P, Any]:
#         @functools.wraps(func)
#         def wrapped(*args: P.args, **kwargs: P.kwargs) -> Any:
#             return func(*args, **kwargs)

#         print(f"Task {name} created", type(wrapped))
#         return wrapped

#     return decorator


# @task()
# def write_code(objective: str) -> str:
#     print(f"Writing code for {objective}")
#     return "code"

# @task()
# def extract_code_with_vars(code: str):
#     print("Extracting code with vars")
#     return "code"

# @task()
# def execute_code(code: str):
#     print("Executing code")
#     return "output"

# # Example usage:
# @workflow("Example Workflow", "This is an example workflow with a single step")
# def plot_graph(a: int = 1, b: str = ""):
#     print("This is the workflow step executing.")
#     logger.info(f"Step parameters: a={a}, b={b}")
#     code = write_code("plot_graph")
#     print(code)


# if __name__ == "__main__":
#     plot_graph(1, "hello")
