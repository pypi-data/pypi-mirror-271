import functools
import warnings


def deprecated_class(cls):
    """Decorator to mark classes as deprecated.

    Example
    -------
    >>> @deprecated_class
    ... class OldClass:
    ...     def __init__(self):
    ...         print("OldClass instance created")
    ...
    >>> old_instance = OldClass()
    OldClass is deprecated.
    OldClass instance created
    """

    @functools.wraps(cls)
    def new_cls(*args, **kwargs):
        warnings.warn(
            f"{cls.__name__} is deprecated.", DeprecationWarning, stacklevel=2
        )
        return cls(*args, **kwargs)

    return new_cls
