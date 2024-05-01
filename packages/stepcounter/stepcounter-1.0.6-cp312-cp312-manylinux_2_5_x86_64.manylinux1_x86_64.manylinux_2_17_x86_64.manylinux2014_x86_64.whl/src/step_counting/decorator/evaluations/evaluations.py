import collections
from types import ModuleType
from typing import Any, Callable, Literal, Optional, Union, Dict
import builtins
import calendar, csv, datetime as dt, fractions, glob, gzip, io, json, io, json, math, os, re, shutil, sys, turtle, zipfile
from http import client
from datetime import date, datetime, timedelta, time
from fractions import Fraction
from csv import DictReader
from io import BytesIO
from zipfile import ZipFile
from collections import deque

from ...non_builtin_types import dict_items_type, dict_keys_type, dict_values_type
from .complexities import ComplexitiesDict

from .builtins.builtins_evaluations import builtins_complexities
from .builtins.bool_evaluations import bool_complexities
from .builtins.bytearray_evaluations import bytearray_complexities
from .builtins.bytes_evaluations import bytes_complexities
from .builtins.complex_evaluations import complex_complexities
from .builtins.dict_evaluations import dict_complexities
from .builtins.dict_keys_evaluations import dict_keys_complexities
from .builtins.dict_items_evaluations import dict_items_complexities
from .builtins.dict_values_evaluations import dict_values_complexities
from .builtins.float_evaluations import float_complexities
from .builtins.frozenset_evaluations import frozenset_complexities
from .builtins.int_evaluations import int_complexities
from .builtins.list_evaluations import list_complexities
from .builtins.memoryview_evaluations import memoryview_complexities
from .builtins.range_evaluations import range_complexities
from .builtins.set_evaluations import set_complexities
from .builtins.slice_evaluations import slice_complexities
from .builtins.str_evaluations import str_complexities
from .builtins.tuple_evaluations import tuple_complexities

from .ib111.calendar_evaluations import calendar_complexities
from .ib111.collections_evaluations import deque_complexities
from .ib111.csv_evaluations import csv_complexities, csv_dictreader_complexities
from .ib111.datetime_evaluations import (
    datetime_complexities,
    datetime_date_complexities,
    datetime_datetime_complexities,
    datetime_time_complexities,
    datetime_timedelta_complexities,
)
from .ib111.fractions_evaluation import (
    fractions_complexities,
    fractions_fraction_complexities,
)
from .ib111.glob_evaluations import glob_complexities
from .ib111.gzip_evaluation import gzip_complexities
from .ib111.httpclient_evaluations import (
    httclient_complexities,
    httclient_HTTPConnection_complexities,
    httclient_HTTPSConnection_complexities,
)
from .ib111.io_evaluations import io_complexities, io_bytesio_complexities
from .ib111.json_evaluations import json_complexities
from .ib111.math_evaluations import math_complexities
from .ib111.os_evaluations import os_complexities
from .ib111.re_evaluations import re_complexities
from .ib111.shutil_evaluations import shutil_complexities
from .ib111.sys_evaluations import sys_complexities
from .ib111.turtle_evaluations import turtle_complexities
from .ib111.zipfile_evaluations import (
    zipfile_complexities,
    zipfile_zipfile_complexities,
)

evaluation_method: Dict[ModuleType, Dict[type | None, ComplexitiesDict]] = {
    builtins: {
        None: builtins_complexities,
        bool: bool_complexities,
        bytearray: bytearray_complexities,
        bytes: bytes_complexities,
        complex: complex_complexities,
        dict: dict_complexities,
        dict_keys_type: dict_keys_complexities,
        dict_items_type: dict_items_complexities,
        dict_values_type: dict_values_complexities,
        float: float_complexities,
        frozenset: frozenset_complexities,
        int: int_complexities,
        list: list_complexities,
        memoryview: memoryview_complexities,
        range: range_complexities,
        set: set_complexities,
        slice: slice_complexities,
        str: str_complexities,
        tuple: tuple_complexities,
    },
    collections: {
        deque: deque_complexities,
    },
    calendar: {None: calendar_complexities},
    csv: {None: csv_complexities, DictReader: csv_dictreader_complexities},
    dt: {
        None: datetime_complexities,
        date: datetime_date_complexities,
        datetime: datetime_datetime_complexities,
        timedelta: datetime_timedelta_complexities,
        time: datetime_time_complexities,
    },
    fractions: {
        None: fractions_complexities,
        Fraction: fractions_fraction_complexities,
    },
    glob: {None: glob_complexities},
    gzip: {None: gzip_complexities},
    client: {
        None: httclient_complexities,
        client.HTTPConnection: httclient_HTTPConnection_complexities,
        client.HTTPSConnection: httclient_HTTPSConnection_complexities,
    },
    io: {None: io_complexities, BytesIO: io_bytesio_complexities},
    json: {None: json_complexities},
    math: {None: math_complexities},
    os: {None: os_complexities},
    re: {None: re_complexities},
    shutil: {None: shutil_complexities},
    sys: {None: sys_complexities},
    turtle: {None: turtle_complexities},
    zipfile: {None: zipfile_complexities, ZipFile: zipfile_zipfile_complexities},
}


def default_evaluation(_: tuple[Any, ...]) -> int:
    """
    Returns default evaluation (1) for functions with unknown evaluation.

    Parameters
    ----------
    _ (Any): parameters of the method with unknown evaluation
    Returns
    -------
    1
    """
    return 1


def get_evaluation_method(
    module: ModuleType, class_: Optional[type], func_name: str
) -> Callable[[tuple[Any, ...]], int]:
    """
    Return evaluation method for given combination of module,
    class and function name.

    Parameters
    ----------
    module (ModuleType): Module which defines the class/method
    class_ (Optional[type]): class which defines the method, None if the
    function is not defined by class
    function_name (str): name of the function

    Returns
    -------
    Function: function for evaluation of given function
    """
    return (
        evaluation_method.get(module, {})
        .get(class_, {})
        .get(func_name, default_evaluation)
    )


def evaluate_record(
    module: ModuleType, class_: Optional[type], func_name: str, args: tuple[Any, ...]
) -> int:
    """
    Gets evaluation method for given combination of module, class and funtion
    name and uses it with given arguments to get evaluation.

    Parameters
    ----------
    module (ModuleType): Module which defines the class/method
    class_ (Optional[type]): class which defines the method, None if the
    function is not defined by class
    function_name (str): name of the function
    args (tuple(Any)): arguments with which the function was called

    Returns
    -------
    None
    """
    if func_name == '__import__':
        return 1

    return get_evaluation_method(module, class_, func_name)(args)
