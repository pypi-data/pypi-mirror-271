"""AttriBox subclasses the TypedDescriptor class and incorporates
syntactic sugar for setting the inner class, and for the inner object
creation. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import Any, Callable
from types import MethodType

from icecream import ic
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from attribox import TypedDescriptor, scope, this

if sys.version_info.minor < 11:
  from typing_extensions import Self
else:
  from typing import Self

ic.configureOutput(includeContext=True, )


class AttriBox(TypedDescriptor):
  """AttriBox subclasses the TypedDescriptor class and incorporates
  syntactic sugar for setting the inner class, and for the inner object
  creation. """

  __positional_args__ = None
  __keyword_args__ = None

  @staticmethod
  def _getterFactory(obj: object, name: str, type_: type) -> MethodType:
    """Returns a function that returns the attribute. """

    def func(self, ) -> Any:
      attribute = getattr(self, name, None)
      if attribute is None:
        raise AttributeError('The attribute is not set!')
      if isinstance(attribute, type_):
        return attribute
      e = typeMsg('attribute', attribute, type_)
      raise TypeError(e)

    return MethodType(func, obj)

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the AttriBox instance. """
    if not kwargs.get('_root', False):
      e = """The AttriBox class should not be instantiated directly!"""
      raise TypeError(e)
    if not args:
      e = """The inner class must be provided. """
      raise TypeError(e)
    innerClass = args[0]
    if not isinstance(innerClass, type):
      e = typeMsg('innerClass', innerClass, type)
      raise TypeError(e)
    self._setInnerClass(innerClass)

  @classmethod
  def __class_getitem__(cls, innerClass: type) -> Self:
    """Syntactic sugar for setting the inner class. """
    return cls(innerClass, _root=True)

  def __call__(self, *args, **kwargs) -> Self:
    """Syntactic sugar for creating an instance of the inner class. """
    self.__positional_args__ = args
    self.__keyword_args__ = kwargs
    return self

  def _getPrivateName(self, ) -> str:
    """Returns the name of the private attribute used to store the inner
    object. """
    return '__%s_value__' % (self._getFieldName(),)

  def _createInnerObject(self, instance: object) -> object:
    """Creates an instance of the inner class. """
    innerClass = self._getInnerClass()
    kwargs = self.__keyword_args__
    args = []
    for arg in self.__positional_args__:
      if arg is this:
        args.append(instance)
      elif arg is scope:
        args.append(self._getFieldOwner())
      else:
        args.append(arg)
    innerObject = innerClass(*args, **kwargs)
    setattr(innerObject, '__outer_box__', self)
    setattr(innerObject, '__owning_instance__', instance)
    setattr(innerObject, '__field_owner__', self._getFieldOwner())
    setattr(innerObject, '__field_name__', self._getFieldName())
    setattr(innerObject,
            'getFieldOwner',
            self._getterFactory('__field_owner__', type))
    setattr(innerObject,
            'getFieldName',
            self._getterFactory('__field_name__', str))
    setattr(innerObject,
            'getOuterBox',
            self._getterFactory('__outer_box__', AttriBox))
    setattr(innerObject,
            'getOwningInstance',
            self._getterFactory('__owning_instance__', object))
    return innerObject

  def _typeGuard(self, item: object) -> Any:
    """Raises a TypeError if the item is not an instance of the inner
    class. """
    innerClass = self._getInnerClass()
    if not isinstance(item, innerClass):
      e = typeMsg('item', item, innerClass)
      raise TypeError(monoSpace(e))

  def __str__(self, ) -> str:
    ownerName = self._getFieldOwner().__name__
    fieldName = self._getFieldName()
    innerName = self._getInnerClass().__name__
    return '%s.%s: %s' % (ownerName, fieldName, innerName)

  def __repr__(self, ) -> str:
    ownerName = self._getFieldOwner().__name__
    fieldName = self._getFieldName()
    innerName = self._getInnerClass().__name__
    args = ', '.join([*self.__positional_args__, *self.__keyword_args__])
    return '%s = AttriBox[%s](%s)' % (fieldName, innerName, args)

  @classmethod
  def _getOwnerListName(cls) -> str:
    """Returns the name at which the list of attribute instances of this
    type. Please note that this name is not unique to the owner as they
    are in separate scopes."""
    return '__boxes_%s__' % cls.__qualname__

  def __set_name__(self, owner: type, name: str) -> None:
    """Sets the name of the field. """
    ownerListName = self._getOwnerListName()
    TypedDescriptor.__set_name__(self, owner, name)
    existing = getattr(owner, ownerListName, [])
    if existing:
      return setattr(owner, ownerListName, [*existing, self])
    setattr(owner, ownerListName, [self, ])
    oldInitSub = getattr(owner, '__init_subclass__')

    def newInitSub(cls, *args, **kwargs) -> None:
      """Triggers the extra init"""
      oldInitSub(*args, **kwargs)
      self.applyBoxes(cls)

    setattr(owner, '__init_subclass__', classmethod(newInitSub))

  @classmethod
  def applyBoxes(cls, owner: type) -> None:
    """Applies the boxes to the owner class."""
    ownerListName = cls._getOwnerListName()
    boxes = getattr(owner, ownerListName, [])
    for box in boxes:
      if not isinstance(box, AttriBox):
        e = typeMsg('box', box, AttriBox)
        raise TypeError(e)
      boxName = box._getFieldName()
      setattr(cls, boxName, box)
      cls.__set_name__(box, owner, boxName)
