import os
import importlib.util


def load_modules_from_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            module_name = filename[:-3]  # Remove the '.py' from filename
            file_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
