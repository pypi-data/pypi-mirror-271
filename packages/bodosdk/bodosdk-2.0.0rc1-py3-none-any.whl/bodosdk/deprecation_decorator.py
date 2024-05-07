import logging
from functools import wraps
from typing import Any


def check_deprecation(func) -> Any:
    """Decorator function."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if func.__name__ in self._deprecated_methods:
            msg = (
                f"Method {func.__name__} of class {self.__class__.__name__} will "
                f"be deprecated in version {self._deprecated_methods[func.__name__].get('version')}. "
                f"Method will be supported till {self._deprecated_methods[func.__name__].get('end_of_support')}. "
                f"Additional notes: {self._deprecated_methods[func.__name__].get('notes')}"
            )
            print(msg)
            logging.warning(msg)
        result = func(self, *args, **kwargs)
        return result

    return wrapper
