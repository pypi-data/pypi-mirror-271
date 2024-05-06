"""
Basic NeuralNetwork that defines Methods for all NeuralNetworks to implement
"""
import numpy as np
import os
import pickle
from abc import ABC, abstractmethod

class BaseNeuralNetwork(ABC):

	"""

	Attributes:
	-----------

	protected:

	self._layers													: container of own layers
	self._compiled													: variable indicating the readiness of the NeuralNetwork i.e. if it is already built completely

	Methods:
	---------

	public:

	@static from_format(list[dict]) -> FeedForwardNeuralNetwork		: builds a NeuralNetwork from a specific format, which can be acquired 
																	: by calling the format method in this class
	format() -> list[dict]											: returns the format with all informations about this NeuralNetwork

	@static load(str) -> FeedForwardNeuralNetwork					: Loads a NeuralNetwork from a file, in which one was previously save by the save method

	save(str, bool override=False)									: Saves this NeuralNetwork into the path given.
																	: If a file with the same name already exists, and override is False, this method will do nothing.

	copy() -> FeedForwardNeuralNetwork								: Returns an identical shallow copy of the NeuralNetwork

	predict(np.array) -> np.array									: Returns the prediction for the given input of shape (inputsize, batchsize)

	train(	X: np.array, Y: np.array, 								: Trains the NeuralNetwork with input matrix X of shape (inputsize, batchsize)
			batchsize: int, epochs: int,							: and label matrix Y of shape (outputsize, batchsize).
			print_after_n_batches: int=None,						: epochs defines how many times the network will train on the data.
			TEST_X: np.array=None, TEST_Y: np.array=None, 			: batchsize states the size of the individual batches the training data willbe divided into.
			print_accuracy=False,									: If batchsize is not given, SGD, i.e. batchsize = 1 will be chosen.
			print_after_percentage=None, 							: If print_after_n_batches is not None, the method train will print out the progress onto sys.stdout.
			print_after_time=None									: What will be printed is the loss and, if print_accuracy=True, the accuracy.
		)															: The training progress in terms of loss and accuracy will be drawn from X and Y if
																	: TEST_X and TEST_Y are None, else they will be drawn from TEST_X and TEST_Y
																	: print_after_percentage is another method of getting the progress printed onto the screen,
																	: if this is set to a float (0.1 = 10%, 0.632 = 63.2%) the progress will
																	: be printed every time the percentage hurdle was reached.
																	: e.g. if print_after_percentage = 0.05 there will be a print after: [5%, 10%, 15%, 20%, ...]
																	: The percentage depends on the full training progress: number_of_datapoints * epochs
																	: print_after_time prints every time [print_after_time] seconds elapsed. 
																	: if you use values < 1, you can print after fractions of seconds.
																	: all print-methods [print_after_n_batches, print_after_percentage, print_after_time]
																	: are exclusive, you can only pick one at a time.
																	

	loss(X: np.array, Y: np.array) -> float							: Returns the loss occurring when predicting the input data X and expecting the label Y
	"""


	"""
	Concept for all NeuralNetworks
	"""

	def __init__(self):

		#container for all layers
		self._layers = []
		#if the network is ready to start learning
		self._compiled = False

	"""
	Every NeuralNetwork should have formatting available to conserve information
	"""

	@staticmethod
	@abstractmethod
	def from_format(used_format: list):
		pass

	@abstractmethod
	def format(self):
		pass


	#pre-implemented save and load functions.
	@classmethod
	def load(cls, path: str):

		#in the path there is a list of formats of layers in order, obtained from from_format
		
		try:

			loaded_format = None
			with open(path, "rb") as f:
				loaded_format = pickle.load(f)

			return cls.from_format(loaded_format)

		except FileNotFoundError:

			print("unable to load from: " + path)

	"""
	Stores the network based off its format in path, 
	won't override already existing file with the same name if override=False.
	"""
	def save(self, path: str, override=False):

		if os.path.isfile(path) and not override: #won't override already existing file
			print("Won't override "+path+"!")
			return

		own_format = self.format()

		with open(path, "wb") as f:
			pickle.dump(own_format, f)


	#basic copy function
	@classmethod
	def copy(self):

		return self.from_format(self.format())

	"""
	All functions every NeuralNetwork should have
	"""

	@abstractmethod
	def predict(self, X: np.array):
		pass

	@abstractmethod
	def train(self, 	X: np.array, Y: np.array, 
						batchsize: int = 1, #X is the input, Y the labels
						epochs: int = 1, 
						TEST_X = None,  TEST_Y = None,
						print_loss=False,
						print_accuracy=False,
						print_after_n_batches: int = None,
						print_after_percentage=None,
						print_after_time=None,
				):

		pass

	@abstractmethod
	def loss(self, X: np.array, Y: np.array) -> float:
		pass



