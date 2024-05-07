from docstring_parser import parse
from botifyme.utils.tools import get_function_details
from loguru import logger

tool_registry = {}


def function(func):
    """Decorator to mark a method as a function of a tool."""
    # Tag the method; no immediate registration in the registry
    func.is_tool_function = True
    logger.info("Adding a function to the registry: " + func.__name__)
    return func


def tool(cls):
    """Decorator to mark a class as a tool and register it along with its functions."""
    cls.is_tool = True  # Tag the class
    # Initialize tool registration with an empty list of functions
    tool_registry[cls.__name__] = {"class": cls, "functions": {}}

    logger.info("Adding a tool to the registry: " + cls.__name__)
    # Iterate over class attributes to find and register tool functions
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and hasattr(attr_value, "is_tool_function"):
            tool_registry[cls.__name__]["functions"][attr_name] = attr_value

    return cls
