""" Package Eule  """

# -*- coding: utf-8 -*-

from __future__ import annotations

# Import adapters first to register them before any adaptation happens
try:
    import eule.adapters.interval_sets  # noqa: F401
except ImportError:
    pass  # interval-sets not installed

from .core import (
    euler_generator,
    euler,
    euler_keys,
    euler_boundaries,
    Euler
)
from .protocols import SetLike
from .registry import register_adapter, register_detector

__author__ = """Bruno Peixoto"""
__email__ = 'brunolnetto@gmail.com'

__all__ = [
    'euler_generator',
    'euler',
    'euler_keys',
    'euler_boundaries',
    'Euler',
    'SetLike',
    'register_adapter',
    'register_detector',
]
