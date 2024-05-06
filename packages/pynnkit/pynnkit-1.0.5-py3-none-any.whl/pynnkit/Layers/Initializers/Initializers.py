"""
Standard initializers.
Take two inputs: input and output sizes, and should return a matrix
of shape: (output_size, input_size)
"""
import numpy as np
from abc import ABC, abstractmethod
from math import sqrt
from .InitializerTypes import InitializerTypes

class Initializer(ABC):

	"""
	All Initializer functions must be derived from this class.

	__call__(dim1, dim2) returns an initialized np.array of shape: (dim1, dim2)
	"""

	def __init__(self):
		pass

	@abstractmethod
	def __call__(self, dim1: int, dim2: int):
		pass

class UniformInitializer(Initializer):

	"""
	Initializes all values in a uniform distribution from start to end
	"""

	def __init__(self, start: float, end: float):

		self._start = start
		self._end = end

	def __call__(self, dim1: int, dim2: int):

		return np.random.uniform(self._start, self._end, (dim1, dim2))

class StaticInitializer(Initializer):

	"""
	Initializes all weights to an assigned value
	"""

	def __init__(self, value: float):
		
		self._value = value

	def __call__(self, dim1: int, dim2: int):

		arr: np.array = np.zeros((dim1, dim2)) + self._value
		return arr

class XavierInitializer(Initializer):

	"""
	Performs Xavier/He Initialization
	"""
	def __init__(self):
		
		self._sq6: float = 2.44948974278 #the square root of six

	def __call__(self, dim1: int, dim2: int):

		denominator: float = sqrt(dim1+dim2)
		fraction: float = (self._sq6 / denominator)

		return np.random.uniform(-fraction, fraction, (dim1, dim2))


InitializerMap: dict = 	{
							InitializerTypes.UNIFORM : UniformInitializer,
							InitializerTypes.STATIC  : StaticInitializer,
							InitializerTypes.XAVIER  : XavierInitializer,
						}