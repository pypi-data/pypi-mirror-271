"""
Standard Feed Forward Neural Network
"""
import numpy as np
import pickle
import os
from time import perf_counter

from ..Layers.BaseLayer import *
from ..Layers.WeightLayer import WeightLayer
from ..Layers.ActivationLayer import ActivationLayer
from ..Layers.LossLayer import LossLayer
from ..Layers.Activation.Activation import *
from ..Layers.Loss.Loss import *
from ..Layers.Initializers.Initializers import *

from ..Layers.Construct import *
from ..Layers.Activation.ActivationTypes import ActivationTypes
from ..Layers.Initializers.InitializerTypes import InitializerTypes
from ..Layers.Loss.LossTypes import LossTypes
from ..Layers.WeightLayerTypes import WeightLayerTypes

from .BaseNeuralNetwork import BaseNeuralNetwork


class FeedForwardNeuralNetwork(BaseNeuralNetwork):

	"""
	Implementation of a FeedForwardNeuralNetwork. Inherits from BaseNeuralNetwork

	IMPORTANT:

	!!!

	Input matrices and label matrices have to be of shape: (inputsize, batchsize)

	!!!

	Attributes:
	-----------



	protected:



	layers: list of all the layers inside the network
	compiled: indicator if this NeuralNetwork is already built, i.e. the last layer was added.

	Methods:
	--------



	protected:



	_construct_layer(size, type, hyperparams)						: actual building process after first defining the input layer. This method is protected.

	_train_batch(self, batch: np.array, label: np.array)			: Trains the network on an indivdual batch. Protected, since this should only be used by the training method.

	_print_training_status(self, X, Y, batches_processed, 
							current_epoch, TEST_X=None, 
							TEST_Y=None, print_accuracy=False)		: Prints the training status out onto sys.stdout 


	public:



	@static from_format(list[dict]) -> FeedForwardNeuralNetwork		: builds a NeuralNetwork from a specific format, which can be acquired 
																	: by calling the format method in this class

	format() -> list[dict]											: returns the format with all informations about this NeuralNetwork. Calls the 
																	: format() method from all layers iteratively to construct the output.

	predict(np.array) -> np.array									: Returns the prediction for the given input of shape (inputsize, batchsize)

	train(	X: np.array, Y: np.array, 								: see: pynnkit/Networks/BaseNeuralNetwork
			batchsize: int, epochs: int,							
																	
			TEST_X: np.array=None, TEST_Y: np.array=None, 		
			print_loss=False,	
			print_accuracy=True
			print_after_n_batches=None,
			print_after_percentage=None,
			print_after_time=None
		)
	
								

	loss(X: np.array, Y: np.array) -> float							: Returns the loss occurring when predicting the input data X and expecting the label Y

	add_layer(	size: int 											: Adds a WeightLayer and a ActivationLayer corresponding to the type_.
				type_: Types.TYPE, hyperparams: dict				: type_ must be from ActivationTypes, hyperparams include WeightLayerTypes instances.

	add_custom_layer(	layer: BaseLayer							: Adds a custom layer, which has to be an instantiated Class derived from 
					)												: NeuralNet.Layers.BaseLayer.BaseLayer.

	add_loss(..Types.LossType)										: Adds the loss and finally compiles the network. The loss must be a specified type from LossTypes.
	
	add_custom_loss(Loss: Loss)										: Adds a custom Loss derived from: NeuralNet.Layers.Loss.Loss

	accuracy(X: np.array, Y: np.array) -> float						: Gives back the accuracy as a probability [0, 1] on input X with labels Y.	

	"""

	def __init__(self):

		super().__init__()
		#memorizing previous layersize, layer construction by calling add_layer with just the size parameter
		self._prev_layersize = -1

	@staticmethod
	def from_format(used_format: list):
		
		back = FeedForwardNeuralNetwork()
		#build_from_format is defined in Format builder, since the function is very complex
		back._layers = build_from_format(used_format)
		
		#If the network has a loss layer, it is already compiled
		if (used_format[-1]["type"] == "LossLayer"):
			back._compiled = True

		return back

	def format(self):
		
		back = []
		#looping over all layers and getting their format
		for layer in self._layers:
			back.append(layer.format())

		return back

	def predict(self, X: np.array):
		
		#prediction can occur without being compiled. Output is what comes out when
		#throwing the data through the network

		x = X.copy()

		for layer in self._layers[:-1]:

			x = layer.forward(x)

		return x

	def _train_batch(self, batch: np.array, label: np.array):

		#storing the batch as the whole first input
		xin = batch

		#saving inputs and outputs for backpropagation
		xinouts = []

		#forward pass
		for el in self._layers[:-1]:

			xout = el.forward(xin)
			xinouts.append((xin, xout))
			xin = xout

		#now xinouts contains the tuple (Input, Output) for every layer

		#backward pass
		#first at the loss layer

		#for storing gradients
		error, grad = self._layers[-1].backward(xin, label)
		#grad does not have to be used to train, since we're checking a loss layer

		#now backward pass over all layers
		for i in range(len(self._layers)-2, -1, -1):

			xin, xout = xinouts[i][0], xinouts[i][1]

			#retreiving error and gradient
			error, grad = self._layers[i].backward(error, xin, xout)

			#if the gradient was not None, this was a Learnable Layer.
			if (grad is not None):

				self._layers[i].update(grad)

	def _print_training_status(self, X, Y, batches_processed, 
									current_epoch, 
									TEST_X=None, 
									TEST_Y=None, 
									print_loss = False, 
									print_accuracy=False, 
									print_percentage=None,
									print_time=None
									):

		"""
		Helper method to print the training status, output method detailed in pynnkit/Networks/BaseNeuralNetwork train method.
		"""

		#data to store the last loss and the last accuracy
		closs = 0.0
		caccuracy = 0.0

		if (print_loss):

			if (TEST_X is None):

				closs = self.loss(X, Y)
				
			else:

				closs = self.loss(TEST_X, TEST_Y)

		if (print_accuracy):

			if (TEST_Y is not None):

				caccuracy = self.accuracy(TEST_X, TEST_Y)

			else:

				caccuracy = self.accuracy(X, Y)

		print("=== Training on batch", batches_processed, "in epoch", (current_epoch+1), "", end="")
		if (print_loss):
			print("with loss", closs, end="")
		if (print_accuracy):
			print("with accuracy", caccuracy, "", end="")
		if (print_percentage):
			print("with percentage of training data: ", print_percentage, "%", end="")
		if (print_time):
			print(f"after training for {print_time}s")
		print("===")



	def train	(self, 	X: np.array, Y: np.array, batchsize: int = 1,
						epochs: int = 1, print_after_n_batches: int = None,
						TEST_X = None, TEST_Y = None,
						print_loss=False,
						print_accuracy=False,
						print_after_percentage=None,
						print_after_time=None,
				):

		"""
		see pynnkit/Networks/BaseNeuralNetwork train method.
		"""

		if (not self._compiled):

			raise RuntimeError("Tried training on an uncompiled Network!")

		if (len(X.shape) != 2):

			print("Your input array(X) shape is", X.shape, "contrary to (?, ?)")
			return

		if (len(Y.shape) != 2):

			print("Your label array(Y) shape is", Y.shape, "contrary to (?, ?)")
			return

		if (TEST_X is not None and len(TEST_X.shape) != 2):

			print("Your test array(TEST_X) shape is", TEST_X.shape, "contrary to (?, ?)")
			return

		if (TEST_Y is not None and len(TEST_Y.shape) != 2):

			print("Your label arrays shape is", TEST_Y.shape, "contrary to (?, ?)")
			return



		#keeping track of the epoch
		current_epoch = 0

		#divding into batches
		sample_size = X.shape[1]

		"""
		All data for percentage calculation
		"""

		#for last percentage update
		next_percentage = print_after_percentage
		all_batches_processed = 0
		number_of_all_batches = sample_size * epochs

		#for time printing purposes
		starttime = perf_counter()
		lasttime = perf_counter()


		#dividing the input X into batches of similiar size, and one batch of leftover training samples
		batches = []
		ybatches = []
		restbatch = None
		restbatchsize = sample_size % batchsize #what's left over
		batches_size = int(sample_size / batchsize) #number of batches of size sample_size

		laststart = 0 #for saving where batches was last indexed

		for i in range(batches_size):

			batches.append(X[:, i*(batchsize):(i+1)*(batchsize)])
			ybatches.append(Y[:, i*(batchsize):(i+1)*(batchsize)])

			laststart = (i+1)*batchsize


		restbatch = X[:, laststart:X.shape[1]]
		restybatch = Y[:, laststart:Y.shape[1]]
		#now all batches and restbatch secured

		#starting the real training process
		while current_epoch < epochs:


			#for knowing how many batches have already been processed
			batches_processed = 0

			#iterating over epochs

			#counter for determining the current batch
			counter = 0 
			#now training with every batch
			for batch in batches:

				self._train_batch(batch, ybatches[counter])
				#increasing counter
				counter += 1

				batches_processed += 1
				all_batches_processed += batchsize

				#record how much time has passed
				nexttime = perf_counter()

				#now, if it is time to print
				if ((print_after_n_batches is not None and not (batches_processed % print_after_n_batches))):


					self._print_training_status(X, Y, batches_processed, current_epoch, TEST_X, TEST_Y, print_loss, print_accuracy)


				elif (print_after_percentage is not None and (all_batches_processed/number_of_all_batches >= next_percentage or all_batches_processed/number_of_all_batches == 1.0)):

					self._print_training_status(X, Y, batches_processed, current_epoch, TEST_X, TEST_Y, print_loss, print_accuracy, all_batches_processed/number_of_all_batches)
					
					#increasing percentage is it was not None and it was a percentage print
					if (print_after_percentage is not None and (all_batches_processed/number_of_all_batches >= next_percentage or all_batches_processed/number_of_all_batches == 1.0)):						
						next_percentage += print_after_percentage

				elif (print_after_time is not None and (nexttime - lasttime) > print_after_time):

					lasttime = nexttime

					self._print_training_status(X, Y, batches_processed, current_epoch, TEST_X, TEST_Y, print_loss, print_accuracy, None, nexttime-starttime)


			#training with restbatch

			if (restbatch.shape[1] != 0):


				self._train_batch(restbatch, restybatch)

				batches_processed += 1
				all_batches_processed += restbatchsize

				#record how much time has passed
				nexttime = perf_counter()

				#now, if it is time to print
				if ((print_after_n_batches is not None and not (batches_processed % print_after_n_batches))):


					self._print_training_status(X, Y, batches_processed, current_epoch, TEST_X, TEST_Y, print_loss, print_accuracy)


				elif (print_after_percentage is not None and (all_batches_processed/number_of_all_batches >= next_percentage or all_batches_processed/number_of_all_batches == 1.0)):

					self._print_training_status(X, Y, batches_processed, current_epoch, TEST_X, TEST_Y, print_loss, print_accuracy, all_batches_processed/number_of_all_batches)
					
					#increasing percentage is it was not None and it was a percentage print
					if (print_after_percentage is not None and (all_batches_processed/number_of_all_batches >= next_percentage or all_batches_processed/number_of_all_batches == 1.0)):						
						next_percentage += print_after_percentage

				elif (print_after_time is not None and (nexttime - lasttime) > print_after_time):

					lasttime = nexttime

					self._print_training_status(X, Y, batches_processed, current_epoch, TEST_X, TEST_Y, print_loss, print_accuracy, None, nexttime-starttime)

			#training completed for this epoch


			current_epoch += 1



	def loss(self, X: np.array, Y: np.array) -> float:
		
		"""
		see pynnkit/Networks/BaseNeuralNetwork
		"""

		x = X.copy()

		for layer in self._layers[:-1]:

			x = layer.forward(x)

		#losslayer forward equates to computing the loss
		return self._layers[-1].forward(x, Y)

	def _construct_layer(self, size, type_, hyperparams):


		#construction methods from NeuralNet.Layers.Construct
		weightlayer = construct_weightlayer(self._prev_layersize, size, hyperparams)
		activationlayer = construct_activationlayer(type_)

		self._layers.append(weightlayer)
		self._layers.append(activationlayer)

	def add_layer(self, size: int, type_: str=None, hyperparams: dict = {}):

		"""
		Hyperparams can include:

		LEARNING_RATE 					: The learning rate. 0.01 by default.
		L2_LAMBDA						: The tikhonov lambda for l2 regularization. 0 by default.
		WEIGHT_INITIALIZER 				: The used weight initializer. Must be derived from Initializer in pynnkit/Layers/Initializers/Initializer.
		BIAS_INITIALIZER 				: The used bias initalizer. Has to be also derived from Initializer in pynnkit/Layers/Initializers/Initializer.

		type_ is one of these activation types:

		SIGMOID
		TANH
		RELU
		SIGN
		LINEAR
		SOFTMAX
		"""

		#checking if trying to add a layer to an already compiled network
		if (self._compiled):

			print("Networks is already compiled!")
			raise RuntimeError("Tried adding a layer to a compiled FeedForwardNeuralNetwork")

		#if self._prev_layersize == -1, this is the first call, i.e. the specification of the input size
		if(self._prev_layersize == -1):
			#setting size for input layer
			self._prev_layersize = size
			return

		#if no activation type was given
		if (self._prev_layersize != -1 and type_ is None):
			print("Unspecified layer")
			raise RuntimeError("Tried adding a layer without specifications")

		if (type_ not in ActivationMap): #ActivationMap from NeuralNet.Layers.Activation.Activation

			print("Your activation type does not seem to be recognized...")
			raise RuntimeError("Incorrect activation type used")
		
		#now constructing
		self._construct_layer(size, type_, hyperparams)
		
		#saving previous layersize
		self._prev_layersize = size


	def add_custom_layer(self, layer, output_size):

		#adds a layer derived from BaseLayer to the network
		#output_size of your neural network for storing purposes
		


		if (self._compiled):

			print("Networks is already compiled!")
			raise RuntimeError("Tried adding a layer to a compiled FeedForwardNeuralNetwork")

		#checking if the layer is an instance of BaseLayer
		if not isinstance(layer, BaseLayer):

			raise RuntimeError(f"the provided layer has to be of type BaseLayer!")

		#no error, append the provided layer and change the output size.
		self._layers.append(layer)
		self._prev_layersize = output_size

	def add_loss(self, losstype):

		"""
		losstype is of type:

		L1_LOSS
		L2_LOSS
		CATEGORICAL_CROSS_ENTROPY_LOSS
		BINARY_CROSS_ENTROPY_LOSS
		SOFTMAX_CROSS_ENTROPY_LOSS
		HINGE_LOSS
		PERCEPTRON_CRITERION
		WESTON_WATKINS_LOSS
		"""
		
		if (self._compiled):

			print("Networks is already compiled!")
			raise RuntimeError("Tried adding a layer to a compiled FeedForwardNeuralNetwork")

		if (losstype not in LossMap): #lossMap from NeuralNet.Layers.Loss.Loss

			print("Your loss type does not seem to be recognized...")
			raise RuntimeError("Incorrect loss type used")

		self._layers.append(construct_losslayer(losstype))
		self._compiled = True #finished building



	def add_custom_loss(self, losslayer):
		
		if (self._compiled):

			print("Networks is already compiled!")
			raise RuntimeError("Tried adding a layer to a compiled FeedForwardNeuralNetwork")


		#checking if the layer is derived from LossLayer
		if not isinstance(losslayer, LossLayer):

			raise RuntimeError("The provided layer has to be derived from LossLayer!")

		#no error, adding the layer and compiling. Now the network is finished
		self._layers.append(losslayer)
		self._compiled = True

	def __str__(self):

		"""
		string representation for the given network
		"""
		
		back: str = ""
		for layer in self._layers[:-1]:

			back += str(layer)+ " -> "
		back += str(self._layers[-1])
		return back

	def accuracy(self, X: np.array, Y: np.array) -> float:
		
		#only reasonable for classification tasks, divides the number of correct maximum outputs through the number of samples

		P = self.predict(X)
		PT = P.T
		YT = Y.T

		rows = YT.shape[0]

		hits = 0
		for i in range(YT.shape[0]):

			if (np.argmax(PT[i]) == np.argmax(YT[i])):
				hits += 1

		acc = hits/rows

		return acc



"""
Classes for BinaryPrediction
"""
class BinaryPerceptron(FeedForwardNeuralNetwork):
	
	"""
	Predefined Types
	"""
	STANDARD = 0
	MSE = 1 # mean squared error
	LOGISTIC_REGRESSION = 2
	SVM_SUPPORT = 3


	"""
	
	Methods:

	__init__(self, inputsize, hyperparams, losstype)		: inputsize determines the number of inputnodes and the size of the input
															: losstype defines the type of loss
															: compatible loss types:
															:
															:	PERCEPTRON_CRITERION
															: 	 
															:
															: hyperparams define the nature of the perceptron
															: Possible hyperparams:
															: [WeightLayerTypes.LEARNING_RATE,
															:  WeightLayerTypes.L2_LAMBDA,
															:  WeightLayerTypes.WEIGHT_INITIALIZER,
															:  WeightLayerTypes.BIAS_INITIALIZER,
															: ]
	"""

	def __init__(self, inputsize: int, hyperparams: dict, decltype=STANDARD):

		super().__init__()

		self.add_layer(inputsize)


		if decltype == BinaryPerceptron.STANDARD:

			#now starting with construction
			self.add_layer(1, SIGN, hyperparams)
			self.add_loss(PERCEPTRON_CRITERION)
			#now already fully compiled

		elif decltype == BinaryPerceptron.MSE:

			#now starting with construction
			self.add_layer(1, SIGN, hyperparams)
			self.add_loss(L2_LOSS)
			#now already fully compiled

		elif decltype == BinaryPerceptron.LOGISTIC_REGRESSION:

			#now starting with construction
			self.add_layer(1, SIGMOID, hyperparams)
			self.add_loss(BINARY_CROSS_ENTROPY_LOSS)
			#now already fully compiled

		elif decltype == BinaryPerceptron.SVM_SUPPORT:

			#now starting with construction
			self.add_layer(1, SIGN, hyperparams)
			self.add_loss(HINGE_LOSS)
			#now already fully compiled

"""
SVM is a variant of the BinaryPerceptron with hinge loss
"""
class SVM(BinaryPerceptron):
	
	def __init__(self, inputsize: int, hyperparams: dict):

		super().__init__(inputsize, hyperparams, BinaryPerceptron.SVM_SUPPORT)
		

"""
Classes for multiclass prediction
"""
class MulticlassPerceptron(FeedForwardNeuralNetwork):
	
	"""
	Classifies data points using the softmax function


	
	Methods:

	__init__(self, inputsize, outputsize, hyperparams, losstype)		: inputsize determines the number of inputnodes and the size of the input
															: losstype defines the type of loss
															: compatible loss types:
															:
															:	PERCEPTRON_CRITERION
															: 	 
															:
															: hyperparams define the nature of the perceptron
															: Possible hyperparams:
															: [WeightLayerTypes.LEARNING_RATE,
															:  WeightLayerTypes.L2_LAMBDA,
															:  WeightLayerTypes.WEIGHT_INITIALIZER,
															:  WeightLayerTypes.BIAS_INITIALIZER,
															: ]
	"""

	def __init__(self, inputsize: int, output_size: int, hyperparams: dict):

		super().__init__()

		self.add_layer(inputsize)
		self.add_layer(output_size, ActivationTypes.SOFTMAX, hyperparams)
		#now already compiled

class WestonWatkinsSVM(FeedForwardNeuralNetwork):
	

	"""
	Defines a Weston-Watkins SVM with its loss function
	
	Methods:

	__init__(self, inputsize, outputsize, hyperparams, losstype)		: inputsize determines the number of inputnodes and the size of the input
															: losstype defines the type of loss
															: compatible loss types:
															:
															:	PERCEPTRON_CRITERION
															: 	 
															:
															: hyperparams define the nature of the perceptron
															: Possible hyperparams:
															: [WeightLayerTypes.LEARNING_RATE,
															:  WeightLayerTypes.L2_LAMBDA,
															:  WeightLayerTypes.WEIGHT_INITIALIZER,
															:  WeightLayerTypes.BIAS_INITIALIZER,
															: ]
	"""

	def __init__(self, inputsize: int, output_size: int, hyperparams: dict):

		super().__init__()

		self.add_layer(inputsize)
		self.add_layer(output_size, ActivationTypes.LINEAR, hyperparams)
		self.add_loss(LossTypes.WESTON_WATKINS_LOSS)

		#now already compiled
