from types import FunctionType, ModuleType
import functools
from typing import Any, Callable, Optional, TypeAlias

from .records.record_classes import (
    SimpleCallRecorder,
    SequnceCallRecorder,
    DetailCallRecorder,
)
from .utils import (
    get_caller_module_info,
    get_method_type,
    module_in_list,
    determine_method,
)

Decorator: TypeAlias = Callable[
    [ModuleType, Optional[type], Callable[..., Any], str], Callable[..., Any]
]


def create_decorator_default(
    tracked_modules: set[ModuleType],
) -> tuple[Decorator, SimpleCallRecorder]:
    """
    Creates a decorated which uses SimpleCallRecorder.

    Parameters
    ----------
    tracked_modules (set): set of tracked modules

    Returns
    -------
    Decorator: decorator
    SimpleCallRecorder:  call recorder for simple call recording
    """
    recorder = SimpleCallRecorder()

    def decorator(
        orig_module: ModuleType,
        class_: Optional[type],
        func: Callable[..., Any],
        func_name: str,
    ) -> Any:
        """
        Decorates given function.

        Parameters
        ----------
        module (ModuleType): Module which defines the class/method
        class_ (Optional[type]): class which defines the method, None if the
        function is not defined by class
        func: function which will be decorated
        funct_name (str): name of the function

        Returns
        -------
        Function: decorated function
        """
        method_type = get_method_type(orig_module, class_, func_name)
        if method_type == classmethod:
            assert hasattr(func, '__func__')
            func_obj = func.__func__
        else:
            func_obj = func

        @functools.wraps(func_obj)
        def wrapper(*args: tuple[Any], **kwargs: tuple[Any]) -> Any:
            module, _ = get_caller_module_info()
            if module_in_list(module, tracked_modules):
                assert module
                recorder.add_record(
                    module, class_, determine_method(func_name, args), args
                )
            return func_obj(*args, **kwargs)

        if method_type in {classmethod, staticmethod}:
            return method_type(wrapper)
        return wrapper

    return decorator, recorder


def create_decorator_sequence(
    tracked_modules: set[ModuleType],
) -> tuple[Decorator, SequnceCallRecorder]:
    """
    Creates a decorated which uses SequenceCallRecorder.

    Parameters
    ----------
    tracked_modules (set): set of tracked modules

    Returns
    -------
    Decorator: decorator
    SequenceCallRecorder:  call recorder for simple call recording
    """
    recorder = SequnceCallRecorder()

    def decorator(
        orig_module: ModuleType,
        class_: Optional[type],
        func: Callable[..., Any],
        func_name: str,
    ) -> Callable[..., Any]:
        """
        Decorates given function.

        Parameters
        ----------
        module (ModuleType): Module which defines the class/method
        class_ (Optional[type]): class which defines the method, None if the
        function is not defined by class
        func: function which will be decorated
        func_name (str): name of the function

        Returns
        -------
        Function: decorated function
        """
        method_type = get_method_type(orig_module, class_, func_name)
        if method_type == classmethod:
            assert hasattr(func, '__func__')
            func_obj = func.__func__
        else:
            func_obj = func

        @functools.wraps(func_obj)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            module, _ = get_caller_module_info()
            if module_in_list(module, tracked_modules):
                assert module
                recorder.add_record(
                    orig_module,
                    class_,
                    determine_method(func_name, args),
                )
            return func_obj(*args, **kwargs)

        if method_type in {classmethod, staticmethod}:
            return method_type(wrapper)  # type: ignore
        return wrapper

    return decorator, recorder


from ..utils.module import get_module_by_name


def create_decorator_detail(
    tracked_modules: set[ModuleType],
) -> tuple[Decorator, DetailCallRecorder]:
    """
    Creates a decorated which uses DetailCallRecorder.

    Parameters
    ----------
    tracked_modules (set): set of tracked modules

    Returns
    -------
    Decorator: decorator
    DetailCallRecorder:  call recorder for simple call recording
    """
    recorder = DetailCallRecorder()

    def decorator(
        orig_module: ModuleType,
        class_: Optional[type],
        func: Callable[..., Any],
        func_name: str,
    ) -> Callable[..., Any]:
        """
        Decorates given function.

        Parameters
        ----------
        module (ModuleType): Module which defines the class/method
        class_ (Optional[type]): class which defines the method, None if the
        function is not defined by class
        func: function which will be decorated
        funct_name (str): name of the function

        Returns
        -------
        Function: decorated function
        """
        method_type = get_method_type(orig_module, class_, func_name)
        if method_type == classmethod:
            assert hasattr(func, '__func__')
            func_obj = func.__func__
        else:
            func_obj = func

        @functools.wraps(func_obj)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            module, line_number = get_caller_module_info()
            if module_in_list(module, tracked_modules):
                assert module
                recorder.add_record(
                    module,
                    line_number,
                    orig_module,
                    class_,
                    func,
                    determine_method(func_name, args),
                    args,
                )

            return func_obj(*args, **kwargs)

        if method_type in {classmethod, staticmethod}:
            return method_type(wrapper)  # type: ignore
        return wrapper

    return decorator, recorder
