"""TypedDescriptor subclasses DelayedDescriptor and adds to it the inner
class. Instances of this class are descriptors that return inner objects
belonging to instances of the owning class. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from vistutils.waitaminute import typeMsg

from attribox import DelayedDescriptor


class TypedDescriptor(DelayedDescriptor):
  """TypedDescriptor subclasses DelayedDescriptor and adds to it the inner
  class. Instances of this class are descriptors that return inner objects
  belonging to instances of the owning class. """

  __inner_class__ = None

  def _getInnerClass(self, ) -> type:
    """Returns the inner class. """
    if self.__inner_class__ is None:
      e = """The inner class has not been assigned. """
      raise AttributeError(e)
    if isinstance(self.__inner_class__, type):
      return self.__inner_class__
    e = typeMsg('__inner_class__', self.__inner_class__, type)
    raise TypeError(e)

  def _setInnerClass(self, innerClass: type) -> None:
    """Sets the inner class. """
    if self.__inner_class__ is not None:
      e = """The inner class has already been assigned. """
      raise AttributeError(e)
    if not isinstance(innerClass, type):
      e = typeMsg('innerClass', innerClass, type)
      raise TypeError(e)
    self.__inner_class__ = innerClass

  def typeGuard(self, item: object) -> None:
    """Raises a TypeError if the item is not an instance of the inner
    class. """
    if not isinstance(item, self._getInnerClass()):
      e = f"""The item is not an instance of the inner class. """
      raise TypeError(e)

  @abstractmethod
  def _createInnerObject(self, instance: object) -> object:
    """Creates an instance of the inner class. """

  @abstractmethod
  def _getPrivateName(self, ) -> str:
    """Returns the name of the private attribute used to store the inner
    object. """
