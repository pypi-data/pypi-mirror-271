"""AltStr provides an alternative to str which does support dynamic
setting of attributes. """
from __future__ import annotations

from typing import Self, Any


class TestList:
  """lMAO"""

  __iter_contents__ = None

  def __init__(self, *args) -> None:
    self.__inner_contents__ = [*args, ]

  def __iter__(self) -> Self:
    """Iteration"""
    self.__iter_contents__ = [*self.__inner_contents__, ]
    return self

  def __next__(self, ) -> Any:
    """Next"""
    try:
      return self.__iter_contents__.pop(0)
    except IndexError as indexError:
      raise StopIteration

  def __len__(self, ) -> int:
    """Length"""
    return len(self.__inner_contents__)

  def __getitem__(self, index: int | str) -> Any:
    """List lookup"""
    if isinstance(index, int):
      n = index % len(self)
      return self.__inner_contents__[n]

  def __setitem__(self, index: int, value: Any) -> None:
    """List set"""
    n = index % len(self)
    self.__inner_contents__[n] = value
