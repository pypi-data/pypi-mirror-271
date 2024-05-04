"""
Some useful abstractions of imports
"""
__version__ = '1.0.1'

import importlib
import importlib.util
from varname import argname
import sys

def lazy_import(name:str):
    """ Import a package upon being used, instead of immediately.
        Useful for packages that want optional dependencies, like this one
        copied from https://docs.python.org/3/library/importlib.html
        If the package isn't installed or can't be found, it returns None
    """
    spec = importlib.util.find_spec(name)
    if spec is None:
        return None
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module

def ensure_imported(package, pip_name:str=...):
    """ A decorator to ensure that `package` is not None, and if it is, raise an ImportError telling
        the user what package needs to be installed. The package is assumed to be the same name as
        the name of the variable passed to package. If it's not, be sure to set `pip_name` to the
        proper value.

        Note that `package` is either a module or None. It's meant to be used with the lazy_import()
        function. This does no actual checking if the package is actually installed or not.

        This decorator only works with functions. To use with a class, decorate __init__()
    """
    name = argname('package')
    # If the installation name isn't specified, assume it's the same as the package name
    if pip_name is Ellipsis:
        pip_name = name

    def decorator(func):
        def decorated_func(*args, **kwargs):
            if package is None:
                raise ImportError(f'Function `{func.__name__}` requires the {name} package. Run `pip install {pip_name}` to resolve this error')
            return func(*args, **kwargs)
        return decorated_func
    return decorator

def try_import(name:str, pip_name:str=..., err:bool=False):
    """ Try to import a package, if it exists. If `err` is True, then it raises an error telling the
        user what package needs to be installed. The package is assumed to be the same name as
        `name`. If it's not, be sure to set `pip_name` to the proper value. If `err` is False, it
        just returns None.
        If `err` is False, `pip_name` is not used.
    """
    try:
        return __import__(name)
    except ImportError as _err:
        if err:
            name = argname('name')
            if pip_name is Ellipsis:
                pip_name = name
            raise ImportError(f"{name} package required. Run `pip install {pip_name}` to resolve this error'") from _err
        else:
            return None
