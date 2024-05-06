
import numpy as np
from abc import ABC, abstractmethod

class BaseLayer(ABC):

	"""


	BaseLayer is the abstract superclass all layers inherit.

	Function forward and backward are used in the prediction and backpropagation
	respectively.
	
	Subclasses should Implement:

	@staticmethod
	construct(params)				:construct this layer from parameters

	forward(X)						: gets an input array and returns an output array
	backward(Error, X_in, X_out)	: returns an tuple of (Error to backwards, list of gradients)

	format()						: returns the format of this Layer as a dict
	from_format(format)				: rebuilds the network from the format

	copy()							: returns a copy of the network
	
	"""

	def __init__(self):
		pass

	@abstractmethod
	def forward(self, X: np.array) -> np.array:
		"""
		Performs a forward pass with input X.
		"""
		pass

	@abstractmethod
	def backward(self, Error: np.array, X_in: np.array, X_out: np.array):
		"""
		Error: error from previous layer
		X_in: matrix of pre-activation values this layer received
		X_out: matrix of post-activation values this layer put out

		returns: (Error: np.array, gradients: list) if there are no gradients, None is the second element of the tuple
		"""
		pass

	@abstractmethod
	def format(self):
		"""
		Gives back a format, which can be used to rebuild 
		this layer
		"""
		pass

	@staticmethod
	@abstractmethod
	def from_format(self):
		"""
		builds this layer from its format
		"""
		pass

	@abstractmethod
	def copy(self):
		"""
		Gives back a snapshot of this specific layer
		"""
		pass

	@abstractmethod
	def __str__(self):
		pass

class LearnableLayer(BaseLayer):

	"""
	Layer with learnable parameters
	"""
	@abstractmethod
	def update(self, gradients: list):
		"""
		updates the parameters. The gradients are in form of a list.
		"""
		pass
