import math
import time
from abc import ABC, abstractmethod
from typing import Optional, Type, List, Iterable

try:
    from tqdm import tqdm
except ImportError:
    from ..mock_ import MockImportObject

    tqdm = MockImportObject("`tqdm` is not installed")  # type:ignore


class ProgressBar(ABC):
    """An interface

    Args:
        ABC (_type_): _description_
    """
    DEFAULT_BAR_FORMAT = "{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}"

    @abstractmethod
    def __init__(self, total, position: int, unit="it", bar_format: str = DEFAULT_BAR_FORMAT, **kwargs) -> None:
        self.total = total
        self.position = position
        self.unit = unit
        self.bar_format = bar_format
        self.num_writes = 0

    @abstractmethod
    def update(self, amount: float = 1) -> None:
        """A function to update the progress-bar's value by a positive relative amount
        """

    @abstractmethod
    def _write(self, *args: str, sep: str = " ", end: str = "\n") -> None: ...

    def write(self, *args: str, sep: str = " ", end: str = "\n") -> None:
        """A function to write additional text with the progress bar
        """
        self._write(*args, sep=sep, end=end)
        self.num_writes += 1

    @abstractmethod
    def reset(self) -> None:
        """A function to reset the progress-bar's progress
       """


ProgressBar.register(tqdm)

__all__ = [
    'ProgressBar',
]
