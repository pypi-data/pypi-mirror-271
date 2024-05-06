# pynnkit
Neural Net Toolkit

# Examples

- [Example for Building a FeedForwardNeuralNetwork](#FeedForwardNeuralNetwork)
- [Example for using built in ML-classes](#BuiltInExample)

## __FeedForwardNeuralNetwork__

Example for learning the XOR function:

```python

import numpy as np
from pynnkit.Networks.FeedForwardNeuralNetwork import FeedForwardNeuralNetwork as NeuralNetwork
from pynnkit.Layers.Construct import *

#XOR data, transposed to be of shape: (inputsize, batchsize)
X = np.array([[0, 0], [1, 0], [0, 1], [1, 1]]).T
Y = np.array([[0, 1], [1, 0], [1, 0], [0, 1]]).T

net = NeuralNetwork()
net.add_layer(2)
net.add_layer(4, SIGMOID, {LEARNING_RATE: 0.1})
net.add_layer(2, SIGMOID, {LEARNING_RATE: 0.1})
net.add_loss(BINARY_CROSS_ENTROPY_LOSS)
#training process
net.train(X, Y, batchsize=4, epochs=50000, print_after_n_batches=1, print_accuracy=True)
#saving the network in the file XORNET.net
net.save("XORNET.net", override=True)
print(net.predict(X).T)
```

Example for training with MNIST-data:

```python
import numpy as np
from pynnkit.Networks.FeedForwardNeuralNetwork import FeedForwardNeuralNetwork as NeuralNetwork
from pynnkit.MNIST.MNIST_Loader import *
from pynnkit.Layers.Construct import *

#loading the flattened data
x_train, y_train, x_test, y_test = MNIST_flat()

net = NeuralNetwork()
net.add_layer(784)
net.add_layer(128, SIGMOID, {LEARNING_RATE: 0.01, L2_LAMBDA: 0.01})
net.add_layer(10, SOFTMAX, {LEARNING_RATE: 0.01, L2_LAMBDA: 0.01})
net.add_loss(CATEGORICAL_CROSS_ENTROPY_LOSS)
#since softmax was added, no further loss is needed
try:

	net.train(x_train, y_train, 10, 1, None, x_test, y_test, print_accuracy=True, print_after_time=2.0)

finally:
	#saving training process
	net.save("MNISTNET", override=True)
```

## __BuildInExample__

