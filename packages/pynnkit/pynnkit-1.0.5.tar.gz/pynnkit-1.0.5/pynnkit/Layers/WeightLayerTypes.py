
#collections of all Types of a WeightLayer, used for construction
from enum import Enum, auto


class WeightLayerTypes(Enum):

	INPUT_SIZE = auto()
	OUTPUT_SIZE = auto()

	WEIGHTS = auto()
	BIASES = auto()

	LEARNING_RATE = auto()
	L2_LAMBDA = auto()
	WEIGHT_INITIALIZER = auto()
	BIAS_INITIALIZER = auto()

