"""AbstractDescriptor outlines the structure required by the descriptor
protocol. It is not intended to be used directly, but to be subclassed by
concrete descriptors. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg


class AbstractDescriptor:
  """AbstractDescriptor outlines the structure required by the descriptor
  protocol. It is not intended to be used directly, but to be subclassed by
  concrete descriptors. """

  __field_name__ = None
  __field_owner__ = None

  def _getFieldName(self) -> str:
    """Returns the name of the field the descriptor is assigned to. """
    if self.__field_name__ is None:
      e = """The descriptor has not been assigned to a field. """
      raise AttributeError(monoSpace(e))
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    e = typeMsg('__field_name__', self.__field_name__, str)
    raise TypeError(monoSpace(e))

  def _getFieldOwner(self) -> type:
    """Returns the type of the class the descriptor is assigned to. """
    if self.__field_owner__ is None:
      e = """The descriptor has not been assigned to a field. """
      raise AttributeError(monoSpace(e))
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    e = typeMsg('__field_owner__', self.__field_owner__, type)
    raise TypeError(monoSpace(e))

  def __set_name__(self, owner: type, name: str) -> None:
    """The __set_name__ method is called when the descriptor is assigned to
    a class attribute. """
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: object, owner: type) -> Any:
    """The __get__ method is called when the descriptor is accessed via the
    owning instance. Subclasses should not override this method, but should
    instead implement the __instance_get__ method. """
    if instance is None:
      return self
    return self.__instance_get__(instance, )

  def __set__(self, instance: object, value: Any) -> None:
    """The __set__ method is called when the descriptor is assigned a value
    via the owning instance. """
    e = """Subclasses may implement the setter and deleter, but the 
    default implementation of __set__ and __delete__ raises the 
    NotImplementedError. """
    raise NotImplementedError(monoSpace(e))

  def __delete__(self, instance: object) -> None:
    """The __delete__ method is called when the descriptor is deleted via
    the owning instance. """
    e = """Subclasses may implement the setter and deleter, but the 
    default implementation of __set__ and __delete__ raises the 
    NotImplementedError. """
    raise NotImplementedError(monoSpace(e))

  @abstractmethod
  def __instance_get__(self, instance: object, owner: type) -> Any:
    """The __instance_get__ method is called when the descriptor is accessed
    via the owning instance. """

  def __str__(self) -> str:
    """This default implementation names the type of the owning class,
    name of the descriptor instance and finally the descriptor field
    type."""
    ownerName = self._getFieldOwner().__name__
    fieldName = self._getFieldName()
    return '%s.%s' % (ownerName, fieldName)
