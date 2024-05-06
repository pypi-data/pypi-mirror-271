"""
Pre-Implemented ActivationLayers:

ReLU
Sigmoid
Sign
Tanh
Linear
Softmax
"""
import numpy as np
from .BaseLayer import BaseLayer
from .Activation.Activation import *
from .Activation.ActivationTypes import ActivationTypes

class ActivationLayer(BaseLayer):


	def __init__(self, activation):

		"""
		Initializes this class with a given activation function.
		The given function function must be a subclass of DerivableFunction
		"""
		
		self._activation_function = activation
		self._activation_function_d = activation.derivative()

	def forward(self, X: np.array):

		"""
		Forward pass of the layer. Passes the given np.array of shape: (input_size, batch_size)
		into the activation function, and returns the result.
		"""
		
		back: np.array = np.zeros_like(X)

		for i in range(X.shape[1]):

			back[:, i] = self._activation_function(X[:, i])

		return back

	def backward(self, Error: np.array, X_in: np.array, X_out: np.array):

		"""
		Backward pass of the layer.
		Returns a tuple with the Error multiplied with he first derivative of the activation function
		as the first parameter, None as the second since this layer does not have changable parameters.

		The derivative of the activation function is in form of a jacobian matrix.
		"""

		#getting the back matrix
		back = np.zeros(Error.shape)

		#computing jacobi for each sample
		for i in range(back.shape[1]):

			colvec = np.dot(self._activation_function_d(X_in[:, i], X_out[:, i]), Error[:, i])
			back[:, i] = colvec

		return (back, None)

	def format(self) -> dict:

		"""
		Returns a dict of form:

		{"type": "ActivationLayer", "function": self._activation_function}
		"""
		
		return {"type": "ActivationLayer", "function": self._activation_function}

	@staticmethod
	def from_format(form):

		"""
		Constructs and returns a ActivationLayer based off a format created via the format method.
		"""

		instantiated_function = form["function"]
		return ActivationLayer(instantiated_function)

	def copy(self):

		"""
		Returns a copy of this layer.
		"""
		
		return ActivationLayer(type(self._activation_function)())

	def __str__(self):
		"""
		Returns a string corresponding to the activation function inside this layer
		"""
		return "["+str(self._activation_function)+"]"
