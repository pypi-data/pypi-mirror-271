"""
"""
import numpy as np
from .BaseLayer import BaseLayer

from .Loss.Loss import *
from .Loss.LossTypes import LossTypes



class LossLayer(BaseLayer):


	def __init__(self, loss):

		"""
		Initizalizes this class with a given lossfunction.
		The lossfunction must be derived from DerivableFunction.
		"""

		self._loss_function = loss
		self._loss_function_d = loss.derivative()

	def forward(self, X: np.array, Y: np.array):
		"""
		computes the overall loss.
		"""
		return self._loss_function(X, Y)
		

	def backward(self, X_in, Y):
		
		"""
		Error and X_out will be None, X_in is the output of the last
		activation layer, therefore X_in will be used together with 
		the derivative of the loss function.
		"""
		return (self._loss_function_d(X_in, Y), None)


	def format(self) -> dict:
		
		"""
		format for determining structure.
		dict of form:

		{"type": "LossLayer", "function": self._loss_function}
		"""
		return {"type": "LossLayer", "function": self._loss_function}

	@staticmethod
	def from_format(form):

		"""
		Builds this layer from a given format, that has been constructed 
		by a previous loss layer.
		"""
		
		instantiated_function = form["function"]
		return LossLayer(instantiated_function)

	def copy(self):

		"""
		returns a copy of this layer.
		"""
		
		return LossLayer(type(self._loss_function)())

	def __str__(self):

		"""
		returns the string representation of this layer,
		depending on the loss function used.
		"""

		return "["+str(self._loss_function)+"]"