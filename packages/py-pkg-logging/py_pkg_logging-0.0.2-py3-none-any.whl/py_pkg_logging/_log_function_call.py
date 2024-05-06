
# -- import packages: ---------------------------------------------------------
import ABCParse
import inspect
from functools import wraps
import logging
import numpy as np


# -- set typing: --------------------------------------------------------------
from typing import Callable


# -- Operational class: -------------------------------------------------------
class FunctionCallLogger(ABCParse.ABCParse):
    def __init__(self, logger):
        """"""
        self.__parse__(locals())
        self._ARGS_IGNORE = ['self']

    @property
    def arg_values(self):
        return self.bound.arguments

    @property
    def cls_method(self):
        return self._args and hasattr(self._args[0], self._logged_func.__name__)

    @property
    def bound(self):
        if self.cls_method:
            self._bound = inspect.signature(self._logged_func).bind(*self._args, **self._kwargs)
        else:
            self._bound = inspect.signature(self._logged_func).bind_partial(*self._args, **self._kwargs)
        self._bound.apply_defaults()
        return self._bound

    @property
    def func_name(self):
        if "self" in self.arg_values:
            cls = self.arg_values.pop("self").__class__.__name__
            return f"{cls}.{self._logged_func.__name__}"
        return self._logged_func.__name__
    
    @property
    def _arg_message(self):
        return_str = ""
        for key, val in self.arg_values.items():
            if not key in self._ARGS_IGNORE:
                if isinstance(val, np.ndarray):
                    val = f"np.ndarray of shape: {val.shape}"
                return_str += f"{key}={val}, "
        return return_str[:-2] # rm final comma
    
    @property
    def log_message(self):
        return f"Called: {self.func_name} with args: {self._arg_message}"


    def __call__(self, logged_func: Callable, *args, **kwargs):
        """ """
        self.__update__(locals())
        self._logger.debug(self.log_message)


# -- API-facing decorator function: -------------------------------------------
def log_function_call(logger):
    """
    Args:
        logger
    """
    def decorator(logged_func: Callable):
        """
        Args:
            logged_func (Callable)
        """
        @wraps(logged_func)
        def wrapper(*args, **kwargs):
            """
            Args:
                *args
                **kwargs
            """
            function_call_logger = FunctionCallLogger(logger = logger)
            function_call_logger(logged_func=logged_func, *args, **kwargs)
            
            return logged_func(*args, **kwargs)
        return wrapper
    return decorator
