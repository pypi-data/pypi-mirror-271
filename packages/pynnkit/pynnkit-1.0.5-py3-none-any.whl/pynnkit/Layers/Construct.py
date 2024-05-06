"""
Handles construction of layers, also includes various type definitions
"""

from .WeightLayer import *
from .ActivationLayer import *
from .LossLayer import *

from .Activation.Activation import *
from .Loss.Loss import *

from .WeightLayerTypes import WeightLayerTypes
from .Loss.LossTypes import LossTypes
from .Activation.ActivationTypes import ActivationTypes
from .Initializers.InitializerTypes import InitializerTypes



def construct_weightlayer(input_size, output_size, hyperparams):
	
	"""
	Constructs a weightlayer from hyperparams.

	Hyperparams:

	WeightLayerTypes.LEARNING_RATE 					: The learning rate. 0.01 by default.
	WeightLayerTypes.L2_LAMBDA						: The tikhonov lambda for l2 regularization. 0 by default.
	WeightLayerTypes.WEIGHT_INITIALIZER 			: The used weight initializer. Must be derived from Initializer.
	WeightLayerTypes.BIAS_INITIALIZER 				: The used bias initalizer. Has to be also derived from Initializer.
	"""

	learning_rate = STANDARD_LEARNING_RATE
	regularization_lambda = STANDARD_REGULARIZATION_LAMBDA
	weight_initializer = STANDARD_WEIGHT_INITIALIZER
	bias_initializer = STANDARD_BIAS_INITIALIZER

	for key in hyperparams.keys():

		original_key = key

		if (key == WeightLayerTypes.LEARNING_RATE):

			learning_rate = hyperparams[original_key]
		
		elif (key == WeightLayerTypes.L2_LAMBDA):

			regularization_lambda = hyperparams[original_key]

		elif (key == WeightLayerTypes.WEIGHT_INITIALIZER):

			weight_initializer = hyperparams[original_key]

		elif (key == WeightLayerTypes.BIAS_INITIALIZER):

			bias_initializer = hyperparams[original_key]

	weightlayer = WeightLayer(input_size, output_size, learning_rate, regularization_lambda, weight_initializer, bias_initializer)

	return weightlayer

def construct_activationlayer(type_):

	"""
	Construct an ActivationLayer from an given ActivationType. Specified in ActivationTypes.
	"""

	return ActivationLayer(ActivationMap[type_]())

def construct_losslayer(losstype):

	"""
	Constructs a LossLayer from a given LossType. Specified in LossTypes.
	"""

	lossfunction = LossMap[losstype]()
	losslayer = LossLayer(lossfunction)
	return losslayer


def build_from_format(format: list) -> list:
	"""
	Builds the layers as a list from the provided formats.
	Formats a gathered by calling the 'format' function on different layers implementing BaseLayer.
	The layers are built back in order and returned as an list of sequential layers.
	"""

	back = []

	for element in format:

		element_type = element["type"]

		if element_type == "ActivationLayer":

			back.append(ActivationLayer.from_format(element))

		elif element_type == "LossLayer":

			back.append(LossLayer.from_format(element))

		elif element_type == "WeightLayer":

			back.append(WeightLayer.from_format(element))

	return back

"""
Quick typedefs for user-friendly variables
"""

#InitializerTypes
UNIFORM = InitializerTypes.UNIFORM
STATIC = InitializerTypes.STATIC
XAVIER = InitializerTypes.XAVIER

#ActivationTypes
SIGMOID = ActivationTypes.SIGMOID
TANH = ActivationTypes.TANH
RELU = ActivationTypes.RELU
SIGN = ActivationTypes.SIGN
LINEAR = ActivationTypes.LINEAR
SOFTMAX = ActivationTypes.SOFTMAX

#LossTypes
L1_LOSS = LossTypes.L1_LOSS
L2_LOSS = LossTypes.L2_LOSS
CATEGORICAL_CROSS_ENTROPY_LOSS = LossTypes.CATEGORICAL_CROSS_ENTROPY_LOSS
BINARY_CROSS_ENTROPY_LOSS = LossTypes.BINARY_CROSS_ENTROPY_LOSS
SOFTMAX_CROSS_ENTROPY_LOSS = LossTypes.SOFTMAX_CROSS_ENTROPY_LOSS
HINGE_LOSS = LossTypes.HINGE_LOSS
PERCEPTRON_CRITERION = LossTypes.PERCEPTRON_CRITERION
WESTON_WATKINS_LOSS = LossTypes.WESTON_WATKINS_LOSS

#WeightLayerTypes
LEARNING_RATE = WeightLayerTypes.LEARNING_RATE
L2_LAMBDA = WeightLayerTypes.L2_LAMBDA
WEIGHT_INITIALIZER = WeightLayerTypes.WEIGHT_INITIALIZER
BIAS_INITIALIZER = WeightLayerTypes.BIAS_INITIALIZER
