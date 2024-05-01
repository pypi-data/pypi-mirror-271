from types import ModuleType

import builtins
import collections
import turtle, typing, math, fractions, gzip, http.client, re, zipfile, io, glob, sys, csv, datetime, calendar, json, shutil, os, sqlite3, random

from .non_builtin_types import (
    dict_items_type,
    dict_keys_type,
    dict_values_type,
)

builtin_methods: list[str] = [
    'print',
    'AssertionError',
    #'AttributeError',
    #'hasattr',
    'sum',
    'enumerate',
    '__build_class__',
    # 'isinstance',
    'open',
]

default_types: dict[ModuleType, set[type]] = {
    builtins: {
        int,
        float,
        complex,
        dict,
        list,
        bool,
        str,
        set,
        frozenset,
        bytes,
        bytearray,
        memoryview,
        tuple,
        slice,
        range,
        dict_items_type,
        dict_keys_type,
        dict_values_type,
    },
    collections: {
        collections.deque,
    },
}

ib111_imports = {
    turtle: {
        'forward',
        'backward',
        'right',
        'left',
        'setheading',
        'done',
        'speed',
        'delay',
        'penup',
        'pendown',
    },
    typing: {
        'Annotated',
    },
    math: {
        'pi',
        'acos',
        'cos',
        'asin',
        'sin',
        'atan',
        'atan2',
        'tan',
        'sqrt',
        'isqrt',
        'degrees',
        'radians',
        'trunc',
        'floor',
        'ceil',
        'isclose',
        'gcd',
        'lcm',
        'factorial',
    },
    fractions: {
        'Fraction',
    },
    gzip: {'open'},
    http.client: {'HTTPSConnection', 'HTTPConnection'},
    re: {'findall', 'match', 'compile', 'sub', 'search'},
    zipfile: {'ZipFile', 'is_zipfile'},
    io: {'BytesIO'},
    glob: {'glob'},
    sys: {'stdin', 'stdout', 'stderr', 'argv'},
    csv: {'reader', 'writer', 'DictReader'},
    datetime: {'date', 'datetime', 'timedelta', 'time'},
    calendar: {'monthrange'},
    json: {'load', 'loads', 'dump', 'dumps'},
    shutil: {'rmtree', 'copyfile'},
    os: {
        'path',
        'remove',
        'getcwd',
        'mkdir',
        'listdir',
        'makedirs',
        'chdir',
        'scandir',
        'rmdir',
        'rename',
    },
    sqlite3: {'connect'},
    random: {
        'Random',
        'seed',
        'randint',
        'random',
        'shuffle',
        'choice',
        'sample',
    },
}
