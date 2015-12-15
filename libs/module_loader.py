import os
from os.path import isfile, basename, dirname, relpath
from traceback import format_exc
import inspect
import importlib

__author__ = 'Joshua D. Katz'


def get_variables(module):
    """
    Get all of the variables defined within a module.

    :param module: The module to inspect.
    :return: A dictionary of strings for the variable name, and values for the value of the variable.
    """

    def is_var(item):
        return not inspect.isfunction(item) and inspect.getmodule(item) is None

    module_attributes = {k: getattr(module, k) for k in module.__dict__.keys()}

    return {k: v for k, v in module_attributes.items() if is_var(v) and not k.startswith("__")}


def is_function(mod, func):
    """
    Check to see if a module attribute is a function.

    :param mod: Module to check ownership of.
    :param func: Attribute who is suspected of being a function.
    :return: True if the module is the owner of the attribute and if the attribute is a function.
    """
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def get_module_functions(mod):
    """
    Get all of the functions defined within a module.

    :param mod: The module to pull functions from.
    :return: A dictionary of function names and their function instances.
    """
    return {func.__name__: func for func in mod.__dict__.values() if is_function(mod, func)}


def load_module(code_path):
    """
    Load a module within this directory tree.
    TODO: Work from any directory.

    :param code_path: The path to a python file.
    :return: None if there is no file at the location, a string if there was an exception thrown or the loaded module.
    """
    if not isfile(code_path):
        return None

    try:

        # Magic module loading
        code_dir = dirname(relpath(code_path))
        code_file = basename(code_path)
        module_path = code_dir.replace(os.sep, ".")
        module_name = code_file[0:code_file.index(".")]

        return importlib.import_module("%s.%s" % (module_path, module_name))  # , fromlist=["*"])

    # Must handle ANY exception.
    # This will come from the module we are loading.
    # Any exception thrown is from the student's code.
    except:

        # print("%s failed to load" % code_path)
        # traceback.format_exec() returns a string.
        # The string is the text that the exception would have been thrown.
        return format_exc()
