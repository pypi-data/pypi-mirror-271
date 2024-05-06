"""
Function, that can give back it's derivative. Used for Loss Functions and Activation Functions
"""
import numpy as np
from abc import ABC, abstractmethod

class DerivativeNotImplementedException(Exception):

	"""
	gets thrown when a user tries to call the derivative() method on an
	Instance of DerivableFunction, but a derivative of this order is not implemented,
	i.e. this is the furthest depth of the derivative() chain.
	"""

	def __init__(self, order: int):

		self._order = order

	def __str__(self):

		return f"there exists no derivative of depth {order}!"

class DerivableFunction(ABC):

	"""
	Function that can be called via (), 
	and gives back another DerivableFunction (its derivative) via derivative().

	self._function is the function this Wrapper uses internally 
	self._order is the order of the Function (0 for normal function, 1 for first derivative, 2 for second...)
	"""

	def __init__(self, function=None):
		"""
		Initializes this class with a given function.
		The given function will be used when this instance is called
		"""
		self._function = function
		self._order = 0

	@abstractmethod
	def __call__(self):
		"""
		Standard Function call
		"""
		pass

	@abstractmethod
	def derivative(self):
		"""
		Gives back the derivative based on the order
		"""
		pass

	@abstractmethod
	def __str__(self):
		"""
		Returns a unique string representation
		"""
		pass

	def set_function(self, function):
		"""
		Changes the given function
		"""
		self._function = function




