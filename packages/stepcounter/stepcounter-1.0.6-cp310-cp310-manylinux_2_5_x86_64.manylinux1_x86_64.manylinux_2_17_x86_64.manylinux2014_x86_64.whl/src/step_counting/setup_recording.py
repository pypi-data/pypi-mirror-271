import builtins
import inspect
import traceback
from types import ModuleType
from typing import Any, Callable, Optional

from .decorator.records.record_classes import DetailCallRecorder
from .ib111_restrictions import default_types, builtin_methods, ib111_imports
from .decorator.decorators import create_decorator_detail, Decorator

from .ignor import ignored_methods, is_ignored
from .patch.patch_imports import import_decorator
from .utils.methods import is_py_method_def
from .patch.patching import (
    create_patch,
    apply,
    revert,
)
from .utils.module import (
    get_module_imports,
    is_user_defined_module,
    get_module_by_name,
)
from .utils.methods import get_c_method

from .ignor import (
    get_def_ignored_modules,
    ignored_specifics,
    ignored_classes,
)


def decorate_builtins(decorator: Decorator) -> None:
    """
    Decorates all builtin methods stored in builtin_method
    with given decorator and creates patches for them.

    Parameters
    ----------
    decorator(Decorator): decorator

    Returns
    -------
    None
    """
    for obj_name in builtin_methods:
        obj = getattr(builtins, obj_name)

        if callable(obj):
            create_patch(
                builtins, None, obj_name, decorator(builtins, None, obj, obj_name)
            )


def decorate_defaults(decorator: Decorator) -> None:
    """
    Decorates all methods of default types and creates patches fro them.

    Parameters
    ----------
    decorator(Decorator): decorator

    Returns
    -------
    None
    """
    for module, classes in default_types.items():
        for class_ in classes:
            for n in dir(class_) + ['comparison']:
                if is_ignored(class_, n):
                    continue

                if is_py_method_def(class_, n):
                    orig_method = getattr(class_, n)
                else:
                    orig_method = get_c_method(class_, n)

                if orig_method is None:
                    raise Exception(
                        f'Unknown method {n} of class {class_.__name__} in module {module.__name__}'
                    )

                if callable(orig_method):
                    create_patch(
                        module,
                        class_.__name__,
                        n,
                        decorator(module, class_, orig_method, n),
                    )


def decorate_class(
    module: ModuleType,
    class_: type,
    decorator: Decorator,
) -> None:
    """
    Decorates all methods of a class from given module and creates patches
    for them.

    Parameters
    ----------
    module (ModuleType): module to which the class belongs
    class_ (type): class whose methods
    decorator(Decorator): decorator

    Returns
    -------
    None
    """
    for name, fn in inspect.getmembers(class_, predicate=inspect.isroutine):
        if not is_ignored(None, name) and class_ not in set.union(
            *default_types.values()
        ):
            create_patch(
                module,
                class_.__name__,
                name,
                decorator(module, class_, fn, name),
            )


def decorate_all_methods_in_module(module: ModuleType, decorator: Decorator) -> None:
    """
    Decorates all methods of a module and method of all classes in the module
    and creates patches for them.

    Parameters
    ----------
    module (ModuleType): module to which the class belongs
    decorator (Decorator): decorator

    Returns
    -------
    None
    """
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if is_ignored(obj, None):
                continue

            decorate_class(module, obj, decorator)

        elif inspect.isroutine(obj):
            create_patch(
                module,
                None,
                name,
                decorator(get_module_by_name(obj.__module__), None, obj, name),
            )


def decorate_ib111_modules(decorator: Decorator) -> None:
    """
    Decorates all modules specific for ib111 preparation.

    Parameters
    ----------
    decorator (Decorator): decorator

    Returns
    -------
    None
    """
    for module, object_names in ib111_imports.items():
        for obj_name in object_names:
            obj = getattr(module, obj_name)
            if inspect.ismodule(obj):
                decorate_all_methods_in_module(obj, decorator)
            if inspect.isclass(obj):
                decorate_class(module, obj, decorator)

            elif inspect.isroutine(obj):
                create_patch(
                    module, None, obj_name, decorator(module, None, obj, obj_name)
                )


def wrap_import(decorator: Decorator, user_defined_modules: set[ModuleType]) -> None:
    """
    This method wrapps import with its designated decorator and creates
    a patch for it.

    Parameters
    ----------
    decorator (Decorator): decorator
    user_define_modules (set): set of all modules defined by user

    Returns
    -------
    None
    """
    import_wrapper = import_decorator(decorator, user_defined_modules)

    create_patch(
        builtins,
        None,
        '__import__',
        decorator(builtins, None, import_wrapper, '__import__'),
    )


def patch_imported_methods(
    imported_callables: set[Callable[..., Any]], decorator: Decorator
) -> None:
    """
    Decorates each imported callable and creates patch(es) for it.

    Parameters
    ----------
    imported_callables (Callable): class or method
    decorator(Decorator): decorator

    Returns
    -------
    None
    """
    for call in imported_callables:
        module = get_module_by_name(call.__module__)
        if inspect.isclass(call):
            if call in set().union(*default_types.values()):
                continue

            decorate_class(module, call, decorator)
        else:
            create_patch(
                module,
                None,
                call.__name__,
                decorator(module, None, call, call.__name__),
            )


def setup_recording(
    module: ModuleType, ignored_modules: set[ModuleType]
) -> tuple[DetailCallRecorder, set[ModuleType]]:
    """
    Performs complete setup of all imported modules, callables.
    Also sets up default types and methods and ib111 specific libraries.

    Parameters
    ----------
    module (ModuleType): original module that will be tested
    ignored_modules (set): set of modules user wishes to not account for
    while recording

    Returns
    -------
    DetailCallRecorded: detailed recorder
    set: set of modules that will be accounted for in the recording
    """
    setup_modules, _ = get_def_ignored_modules()
    ignored_modules.update(setup_modules)
    module_imports, imported_callables = get_module_imports(module, ignored_modules)

    user_defined_modules = {
        import_ for import_ in module_imports if is_user_defined_module(import_)
    }

    user_defined_callables = set()
    for call in imported_callables:
        call_module = get_module_by_name(call.__module__)
        if is_user_defined_module(call_module):
            user_defined_callables.add(call)
            user_defined_modules.add(call_module)
    user_defined_modules.add(module)

    # Filter out ignored modules
    user_defined_modules = {
        module for module in user_defined_modules if module not in ignored_modules
    }

    decorator, recorder = create_decorator_detail(user_defined_modules)

    wrap_import(decorator, user_defined_modules)

    patch_imported_methods(user_defined_callables, decorator)
    for module in user_defined_modules:
        decorate_all_methods_in_module(module, decorator)

    decorate_defaults(decorator)
    decorate_builtins(decorator)
    decorate_ib111_modules(decorator)

    return recorder, user_defined_modules


class RecodingActivated:
    """
    A class representing a state of the recording
    This classed is used for simplification of the recording process.
    All patches are applied upon entering and reverted on exit.
    """

    def __enter__(self) -> None:
        """
        Applies all patches.

        Returns
        -------
        None
        """
        apply()

    def __exit__(
        self,
        type: Optional[BaseException],
        value: Optional[BaseException],
        traceback: Optional[traceback.TracebackException],
    ) -> None:
        """
        Reverts all patches.

        Returns
        -------
        None
        """
        revert()
