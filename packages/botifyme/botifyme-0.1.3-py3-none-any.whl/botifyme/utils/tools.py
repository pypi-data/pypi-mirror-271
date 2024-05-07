import inspect
from docstring_parser import parse

def get_function_details(func):
    """Extract details from a function, including its name, description, and parameter info."""
    docstring = inspect.getdoc(func)
    parsed_docstring = parse(docstring)

    func_details = {
        "name": func.__name__,
        "description": parsed_docstring.short_description,
        "parameters": {"type": "object", "properties": {}, "required": []},
    }

    sig = inspect.signature(func)
    for param in sig.parameters.values():
        
        param_name = param.name
        
        if param_name == "self":
            continue
        
        param_doc = next(
            (p for p in parsed_docstring.params if p.arg_name == param_name), None
        )

        param_type = (
            str(param_doc.type_name)
            if param.annotation != inspect.Parameter.empty
            else "string"
        )
        
        if param_type == "int":
            param_type = "number"
            
        if param_type == "str":
            param_type = "string"
            
        if param_type == "bool":
            param_type = "boolean"
            
        if param_type == "float":
            param_type = "number"
            
        if param_type == "list":
            param_type = "array"

        # Determine if parameter is optional based on its default value
        is_optional = param.default != inspect.Parameter.empty
        param_desc = param_doc.description if param_doc else ""

        # Add parameter details to the function details dictionary
        func_details["parameters"]["properties"][param_name] = {
            "type": param_type,
            "description": param_desc,
        }

        # If the parameter is required (no default value), add it to the required list
        if not is_optional:
            func_details["parameters"]["required"].append(param_name)
        else:
            # For optional parameters, include the default value if available
            func_details["parameters"]["properties"][param_name]["default"] = (
                param.default if param.default != inspect.Parameter.empty else None
            )

    # Optionally, add return type info if needed
    if parsed_docstring.returns:
        func_details["return"] = {
            "type": (
                parsed_docstring.returns.type_name
                if parsed_docstring.returns.type_name
                else "unknown"
            ),
            "description": parsed_docstring.returns.description,
        }

    return func_details

def get_class_details(cls):
    """Extract details from a class, including its name, description, and registered functions."""
    docstring = inspect.getdoc(cls)
    parsed_docstring = parse(docstring)

    class_details = {
        "name": cls.__name__,
        "description": parsed_docstring.short_description,
    }

    return class_details

def get_registered_functions_for_class(cls):
    """
    Retrieve all registered functions for a given class.

    Args:
        cls: The class object to inspect.

    Returns:
        A dictionary with function names as keys and function objects as values.
    """
    registered_functions = {}
    # Inspect all members of the class
    for name, member in inspect.getmembers(cls, predicate=inspect.isfunction):
        # Check if the member function is registered in the `function` registry
        if member in function.items():
            registered_functions[name] = member
    return registered_functions
