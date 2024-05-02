"""The 'attribox' package provides an interface between custom classes
owning attributes belonging to other classes. Normally, to achieve this
the class providing an attribute for the owning class are required to
implement accessor methods. This package provides a convenient wrapper
that can be applied to existing classes allowing them to become attributes
other classes without requiring implementation of accessor methods. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._this_scope import this, scope, Singleton
from ._abstract_descriptor import AbstractDescriptor
from ._delayed_descriptor import DelayedDescriptor
from ._typed_descriptor import TypedDescriptor
from ._attri_box import AttriBox
