"""DelayedDescriptor subclasses the AbstractDescriptor class and adds to
it the deferred object creation allowing instantiation of the inner class
to occur on an instance by instance basis.

Please note the nomenclature hierarchy:
  owner class > owner instance > dedicated instance of inner class
Since the name 'instance' firmly belongs to the instance of the owner class,
the name 'inner object' or similar is used to refer to the instance of the
inner class. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from icecream import ic
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from attribox import AbstractDescriptor

ic.configureOutput(includeContext=True)


class DelayedDescriptor(AbstractDescriptor):
  """DelayedDescriptor subclasses the AbstractDescriptor class and adds to
  it the deferred object creation allowing instantiation of the inner class
  to occur on an instance by instance basis.

  Please note the nomenclature hierarchy:
    owner class > owner instance > dedicated instance of inner class
  Since the name 'instance' firmly belongs to the instance of the owner
  class,
  the name 'inner object' or similar is used to refer to the instance of the
  inner class. """

  @abstractmethod
  def _createInnerObject(self, instance: object) -> object:
    """Creates an instance of the inner class. Please note that the
    subclass implementation will receive only the instance for whom to
    create the inner object. Subclasses must be able to create the inner
    object from the information provided up to this point. """

  @abstractmethod
  def _getPrivateName(self, ) -> str:
    """Returns the name of the private attribute used to store the inner
    object. Subclasses must implement this method to define the name on
    the instance of the owner class where the inner object is stored.
    Please note that this class does now define that the getter function
    should definitely point to the contents at a private name. This does
    remove some flexibility to create virtual attributes that does not
    reflect an actual object. """

  def _typeGuard(self, item: object) -> Any:
    """Optional type guard. Subclasses may implement this method to enforce
    type constraints on the inner object. If the inner object does not
    conform to the type constraints, the method should raise a TypeError,
    otherwise it is ignored. """

  def __instance_get__(self, instance: object, **kwargs) -> Any:
    """The __instance_get__ method is called when the descriptor is accessed
    via the owning instance. If the instance already own an inner object,
    the inner object is returned. Otherwise, an inner object is created
    and assigned to the instance after which the method recursively calls
    itself to return the inner object. If for whatever reason the creation
    of the inner object fails, this is caught as a RecursionError."""
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      innerObject = self._createInnerObject(instance)
      setattr(instance, pvtName, innerObject)
      return self.__instance_get__(instance, _recursion=True)
    innerObject = getattr(instance, pvtName, None)
    if innerObject is None:
      e = """Failed to create inner object!"""
      raise AttributeError(e)
    self._typeGuard(innerObject)
    return innerObject
