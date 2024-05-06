
#all supported native activation types

from enum import Enum, auto

class ActivationTypes(Enum):

	SIGMOID = auto()
	TANH = auto()
	RELU = auto()
	SIGN = auto()
	LINEAR = auto()
	SOFTMAX = auto()