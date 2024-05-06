"""
Most basic layer. Used to learn weights and biases.
"""
import numpy as np
from .BaseLayer import BaseLayer, LearnableLayer
from .Initializers.Initializers import *
from .WeightLayerTypes import WeightLayerTypes


#STANDARD DEFINITIONS
STANDARD_LEARNING_RATE: float = 0.01
STANDARD_REGULARIZATION_LAMBDA: float = 0.0
STANDARD_WEIGHT_INITIALIZER: XavierInitializer = XavierInitializer()
STANDARD_BIAS_INITIALIZER: StaticInitializer = StaticInitializer(0)

class WeightLayer(LearnableLayer):


	def __init__(self, 	input_size: int, output_size: int, learning_rate: float = 0.01,\
						l2_lambda: float = 0.0, weight_initializer = STANDARD_WEIGHT_INITIALIZER, bias_initializer = STANDARD_BIAS_INITIALIZER
						):
		"""
		input_size, output_size: number of input data/output neurons
		learning_rate: -
		reg_lambda: tikhonov lambda used for in layer regularization
		weight_initializer, bias_initiliazer: common initializers, standard: Uniform distribution from -1 to 1 for weights,
											  set to 0 for biases

		"""

		self._W = weight_initializer(output_size, input_size) #weights
		self._B = bias_initializer(output_size, 1) #biases

		self._l2_lambda = l2_lambda
		self._learning_rate = learning_rate

		self._input_size = input_size
		self._output_size = output_size

	def forward(self, X: np.array):

		"""
		forward pass of this network, of the form:

		(np.dot(self._W, X) + self._B)
		"""
		
		return (np.dot(self._W, X) + self._B)

	def backward(self, Error: np.array, X_in: np.array, X_out: np.array):

		"""
		computes the backwards error and the gradients to update this layer.

		Computations of form:

		avg_error = np.mean(Error, axis=1, keepdims=True)

		dWeight = np.dot(Error, X_in.T) / Error.shape[1]
		dX = np.dot(self._W.T, Error)
		"""

		avg_error = np.mean(Error, axis=1, keepdims=True)

		dWeight = np.dot(Error, X_in.T) / Error.shape[1]#averaging over batchsize
		dX = np.dot(self._W.T, Error)

		return (dX, [avg_error, dWeight])

	def update(self, gradients: list):

		"""
		Updates the gradients. Updates of form:

		elf._B = self._B * (1 - self._learning_rate * self._l2_lambda) - self._learning_rate * avg_error
		self._W = self._W * (1 - self._learning_rate * self._l2_lambda) - self._learning_rate * dWeight
		"""

		avg_error, dWeight = gradients[0], gradients[1]
		
		self._B = self._B * (1 - self._learning_rate * self._l2_lambda) - self._learning_rate * avg_error
		self._W = self._W * (1 - self._learning_rate * self._l2_lambda) - self._learning_rate * dWeight


	def format(self):

		"""
		Returns a reconstructible format of a snapshot of this layer.
		Returns a dict of form:

					{
						"type": "WeightLayer",
						WeightLayerTypes.INPUT_SIZE: self._input_size,
						WeightLayerTypes.OUTPUT_SIZE: self._output_size,
						WeightLayerTypes.LEARNING_RATE: self._learning_rate,
						WeightLayerTypes.L2_LAMBDA: self._l2_lambda,
						WeightLayerTypes.WEIGHTS: self._W.tolist(),
						WeightLayerTypes.BIASES: self._B.tolist(),
					}
		"""
		
		return 		{
						"type": "WeightLayer",
						WeightLayerTypes.INPUT_SIZE: self._input_size,
						WeightLayerTypes.OUTPUT_SIZE: self._output_size,
						WeightLayerTypes.LEARNING_RATE: self._learning_rate,
						WeightLayerTypes.L2_LAMBDA: self._l2_lambda,
						WeightLayerTypes.WEIGHTS: self._W.tolist(),
						WeightLayerTypes.BIASES: self._B.tolist(),
					}

	@staticmethod
	def from_format(form):

		"""
		Construct a weight layer from the given format, created by a previous WeightLayer
		"""
		input_size = form[WeightLayerTypes.INPUT_SIZE]
		output_size = form[WeightLayerTypes.OUTPUT_SIZE]
		learning_rate = form[WeightLayerTypes.LEARNING_RATE]
		l2_lambda = form[WeightLayerTypes.L2_LAMBDA]

		Layer = WeightLayer(input_size, output_size, learning_rate, l2_lambda)

		weights = np.array(form[WeightLayerTypes.WEIGHTS])
		biases = np.array(form[WeightLayerTypes.BIASES])

		Layer.set_weights(weights)
		Layer.set_biases(biases)

		return Layer

	def copy(self):

		"""
		Returns a shallow copy of this layer.
		"""
		
		back: WeightLayer = WeightLayer(self._input_size, self._output_size, self._learning_rate, self._l2_lambda)
		back.set_weights(self._W.copy())
		back.set_biases(self._B.copy())

		return back

	def set_learning_rate(self, new_rate):
	
		self._learning_rate = new_rate

	def get_learning_rate(self):

		return self._learning_rate

	def set_weights(self, W: np.array):

		self._W = W

	def get_weights(self):

		return self._W

	def set_biases(self, B: np.array):

		self._B = B

	def get_biases(self):

		return self._B

	def set_l2_lambda(self, l2_lambda: float):
	
		self._l2_lambda = l2_lambda

	def get_l2_lambda(self):

		return self._l2_lambda


	def __str__(self):

		"""
		Returns a string representing this layer, 
		based off of: the input size and the output size
		"""
		
		return "[("+str(self._input_size)+"x"+str(self._output_size)+") Layer]"