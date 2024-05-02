"""The singleton class 'this' provides a way of specifying the instance
when creating an AttriBox. It refers to the instance yet to be created."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.metas import AbstractMetaclass, Bases


class Singleton(AbstractMetaclass):
  """Singleton metaclass for AttriBox."""

  __singleton_instance__ = None

  def __init__(cls, name: str, bases: Bases, namespace: dict,
               **kwargs) -> None:
    """Initialize the class."""
    AbstractMetaclass.__init__(cls, name, bases, namespace, **kwargs)
    self = AbstractMetaclass.__call__(cls, )
    setattr(cls, '__singleton_instance__', self)

  def __call__(cls, *args, **kwargs) -> type:
    """Create an instance of the class."""
    return cls.__singleton_instance__


class this(metaclass=Singleton):
  """The singleton class 'this' is a placeholder for the instance about to
  receive an inner object. During creation of inner object,
  each occurrence is replaced by the instance receiving the inner object."""

  def __str__(self) -> str:
    return 'this'


class scope(metaclass=Singleton):
  """The singleton class 'scope' is a placeholder for the owner of the
  instance about to receive an inner object. During creation of inner
  object, each occurrence is replaced by the owner of the instance."""

  def __str__(self) -> str:
    return 'scope'
