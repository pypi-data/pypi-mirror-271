import importlib.util
import inspect
import os
import sys


def find_subclasses(directory, class_name):
    """Find all subclasses of a given class within modules in the specified directory."""
    subclasses = []

    # Ensure the directory is in sys.path for relative imports
    sys.path.insert(0, directory)

    for filename in os.listdir(directory):
        if filename.endswith(".py") and not filename.startswith("__"):
            # Create a full module name from the file name
            module_name = filename[:-3]  # Strip the .py at the end
            file_path = os.path.join(directory, filename)

            # Import the module
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Inspect all classes defined within the module
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Check if the class is a subclass of the target class
                # This assumes class_name is globally available or passed somehow
                if obj != class_name and issubclass(obj, class_name):
                    subclasses.append(obj)

    # Clean up sys.path
    sys.path.remove(directory)

    return subclasses
