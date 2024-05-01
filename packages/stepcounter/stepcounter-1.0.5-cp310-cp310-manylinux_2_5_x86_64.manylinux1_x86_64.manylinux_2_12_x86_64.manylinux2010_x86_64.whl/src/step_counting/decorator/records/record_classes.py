from types import ModuleType
from typing import Any, Callable, Optional, TypeAlias

from step_counting.utils.module import get_module_by_name
from ..evaluations.evaluations import evaluate_record

from ...original_methods import dict_get, list_append

RecordKey: TypeAlias = tuple[ModuleType, Optional[type], str]
SequenceRecords: TypeAlias = list[tuple[ModuleType, str, str]]
ModuleDetailRecords: TypeAlias = dict[int, dict[RecordKey, 'Counter']]
DetailRecords: TypeAlias = dict[ModuleType, ModuleDetailRecords]
########################################################################################
# These methods are used with patches applied. Even through it is not necessary
# to use original methods, they are used for optimization.
########################################################################################


class Counter:
    """
    A class representing a counter.

    Attributes
    ----------
    count_total (int): counts number of operations
    evaluation_total (int): sum of all evaluations
    """

    def __init__(self, count: int = 0, evaluation: int = 0) -> None:
        """
        Initializes a new Counter instance.

        Parameters
        ----------
        count (int): total count of operations
        evaluation (int): sum of evaluations of operations

        Returns
        -------
        None
        """
        self.count_total = count
        self.evaluation_total = evaluation

    def increase(self, evaluation_total: int) -> None:
        """
        Increases the total count_total by 1 and evaluation_total
        bi given evaluation.

        Parameters
        ----------
        evaluation (int): sum of evaluations of operations

        Returns
        -------
        None
        """
        self.count_total = int.__add__(self.count_total, 1)
        self.evaluation_total = int.__add__(self.evaluation_total, evaluation_total)

    def get_count_total(self) -> int:
        """
        Returns count of all operations.

        Returns
        -------
        int: Count of all operations
        """
        return self.count_total

    def get_evaluation_total(self) -> int:
        """
        Returns evaluation of all operations.

        Returns
        -------
        int: Evaluation of all operations
        """
        return self.evaluation_total

    def clear(self) -> None:
        """
        Resets count and evaluation back to 0s.

        Returns
        -------
        None
        """
        self.count_total = 0
        self.evaluation_total = 0

    def __str__(self) -> str:
        """
        Returns string representation of counter

        Returns
        -------
        str: string representation of counter
        """
        return f'(Counter {self.count_total}, {self.evaluation_total})'


class SimpleCallRecorder:
    """
    A class representing a simple recorder. This class only holds one counter
    which is used for all operations.

    Attributes
    ----------
    counter (Counter): Counter for all operations
    """

    def __init__(self) -> None:
        """
        Initializes a new SimpleCallRecorder instance.

        Returns
        -------
        None
        """
        self.counter = Counter()

    def add_record(
        self,
        orig_module: ModuleType,
        cls: Optional[type],
        func_name: str,
        arguments: Any,
    ) -> None:
        """
        Evaluates record and increases the counter accordingly.

        Parameters
        ----------
        orig_module (ModuleType): module where the function was used
        cls (Optional[type]): class if the function belongs to a class,
        None otherwise
        func_name (str): name of the function
        arguments (Any): arguments with which the function was called
        Returns
        -------
        None
        """
        self.counter.increase(evaluate_record(orig_module, cls, func_name, arguments))

    def get_data(self) -> Counter:
        """
        Returns counter.

        Returns
        -------
        Counter: Counter with number of calls and sum of evaluations
        """
        return self.counter

    def evaluate_data(self) -> int:
        """
        Returns sum of evaluations.

        Returns
        -------
        int: sum of evaluations
        """
        return self.counter.get_evaluation_total()

    def clear_data(self) -> None:
        """
        Clears the counter (resets its value to 0s).

        Returns
        -------
        None
        """
        self.counter.clear()


class SequnceCallRecorder:
    """
    A class representing a sequence recorder. This class hold list of
    function calls.

    Attributes
    ----------
    records (list): list of function calls
    """

    def __init__(self) -> None:
        """
        Initializes a new SequnceCallRecorder instance.

        Returns
        -------
        None
        """
        self.records: SequenceRecords = []

    def add_record(
        self, module: ModuleType, class_: Optional[type], func_name: str
    ) -> None:
        """
        Appends the function call to the list.

        Parameters
        ----------
        module (ModuleType): module where the function was used
        class_ (Optional[type]): class if the function belongs to a class,
        None otherwise
        func_name (str): name of the function
        Returns
        -------
        None
        """
        list_append(self.records, (module, class_, func_name))  # type: ignore

    def get_data(self) -> list[tuple[ModuleType, str, str]]:
        """
        Returns collected data.

        Returns
        -------
        list: list with ordered calls of functions
        """
        return self.records.copy()

    def evaluate_data(self) -> int:
        """
        Returns length of records.

        Returns
        -------
        int: length of records
        """
        return len(self.records)

    def clear_data(self) -> None:
        """
        Clears all data.

        Returns
        -------
        None
        """
        self.records.clear()


class DetailCallRecorder:
    """
    A class representing a detail recorder. Holds data of function calls
    in modules and lines with their Counters.

    Attributes
    ----------
    records (dict): list of function calls
    """

    def __init__(self) -> None:
        """
        Initializes a new DetailRecords instance.

        Returns
        -------
        None
        """
        self.records: DetailRecords = dict()

    def add_record(
        self,
        module: ModuleType,
        line_number: int,
        orig_module: ModuleType,
        cls: Optional[type],
        func: Callable[..., Any],
        func_name: str,
        arguments: Any,
    ) -> None:
        """
        Determines method, gets evaluation and creates or increments
        the counter for this function on given line.

        Parameters
        ----------
        module (ModuleType): module where the function was used
        line_number (int): line where the function was used
        orig_module (ModuleType): module where the function was created
        cls (Optional[type]): class if the function belongs to a class,
        func (Function): function which was called
        func_name (str): name of the function (Some function objects do not
        allow to extract name)
        Returns
        -------
        None
        """
        fn_class = getattr(func, '__objclass__', cls)
        fn_module_name = getattr(fn_class, '__module__', None)
        fn_module = get_module_by_name(fn_module_name) if fn_module_name else module

        record_eval = evaluate_record(fn_module, fn_class, func_name, arguments)
        module_records = dict_get(self.records, module, None)

        if module_records is None:
            records: dict[int, dict[RecordKey, Counter]] = {
                line_number: {(orig_module, cls, func_name): Counter(1, record_eval)}
            }
            dict.__setitem__(
                # mypy gets confused with dunder method use
                self.records,
                module,
                records,
            )
            return

        # mypy gets confused with dunder method use
        line_records: Optional[dict[tuple[type, str], Counter]] = dict_get(
            module_records, line_number, None
        )  # type: ignore
        if line_records is None:
            dict.__setitem__(
                module_records,
                # mypy gets confused with dunder method use
                line_number,
                {(orig_module, cls, func_name): Counter(1, record_eval)},
            )
            return

        method_counter = dict_get(line_records, (orig_module, cls, func_name), None)  # type: ignore
        if method_counter is None:
            method_counter = Counter()

        method_counter.increase(record_eval)
        dict.__setitem__(line_records, (orig_module, cls, func_name), method_counter)  # type: ignore

    def get_data(self) -> DetailRecords:
        """
        Returns copy of collected data.

        Returns
        -------
        DetailRecords: records for each module-line-function
        """
        return self.records.copy()

    def evaluate_data(self) -> int:
        """
        Returns collective evaluation of all records.

        Returns
        -------
        int: sum of all evaluations
        """
        score = 0
        for module_records in self.records.values():
            for line_records in module_records.values():
                for counter_ in line_records.values():
                    score += counter_.get_evaluation_total()

        return score

    def clear_data(self) -> None:
        """
        Clears all recorded data.

        Returns
        -------
        None
        """
        self.records.clear()
