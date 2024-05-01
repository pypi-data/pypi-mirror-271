from typing import Any, Generator


def make_generator() -> Generator[None, Any, None]:
    yield None


async def make_async() -> None:
    pass


dict_keys_type = type({}.keys())  # type: ignore
dict_items_type = type({}.items())  # type: ignore
dict_values_type = type({}.values())  # type: ignore
generator_type = type(make_generator())

bytes_iter_type = type(iter(bytes()))
bytearray_iter_type = type(iter(bytearray()))
list_iter_type = type(iter(list()))  # type: ignore
dict_iter_type = type(iter(dict()))  # type: ignore
set_iter_type = type(iter(set()))  # type: ignore
tuple_iter_type = type(iter(tuple()))  # type: ignore


non_builtin_types = {
    'dict_keys': dict_keys_type,
    'dict_items': dict_items_type,
    'dict_values': dict_values_type,
    'generator': generator_type,
    'bytes_iter': bytes_iter_type,
    'bytearray_iter': bytearray_iter_type,
    'list_iterator': list_iter_type,
    'dict_keyiterator': dict_iter_type,
    'bytes_iter': bytes_iter_type,
    'set_iter': set_iter_type,
    'tuple_iterator': tuple_iter_type,
}
