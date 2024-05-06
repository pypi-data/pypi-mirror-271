"""
Setup file for PYPI
"""
from setuptools import setup, find_packages
import os.path

setup(
    name='pynnkit',
    version='1.0.5',
    author='Paul Walcher',
    author_email='paulwalcher12@gmail.com',
    description='Neural Network Kit',
    packages=["pynnkit", "pynnkit.Layers", "pynnkit.MNIST",
                "pynnkit.Networks",
                "pynnkit.Layers.Activation",
                "pynnkit.Layers.Loss",
                "pynnkit.Layers.Initializers",
             ],
    include_package_data=True,
    data_files=[
            
                            (os.path.join("pynnkit","MNIST", "archive"), 
                                        [
                                        os.path.join("pynnkit","MNIST", "archive", "t10k-images.idx3-ubyte"),
                                        os.path.join("pynnkit","MNIST", "archive", "t10k-labels.idx1-ubyte"),
                                        os.path.join("pynnkit","MNIST", "archive", "train-images.idx3-ubyte"),
                                        os.path.join("pynnkit","MNIST", "archive", "train-labels.idx1-ubyte"),
                                        ]
                            ),
                            (os.path.join("pynnkit","MNIST", "archive", "t10k-images-idx3-ubyte"), 
                                        [
                                        os.path.join("pynnkit","MNIST", "archive", "t10k-images-idx3-ubyte", "t10k-images-idx3-ubyte")
                                        ]
                            ),
                            (os.path.join("pynnkit","MNIST", "archive", "t10k-labels-idx1-ubyte"), 
                                        [
                                        os.path.join("pynnkit","MNIST", "archive", "t10k-labels-idx1-ubyte", "t10k-labels-idx1-ubyte") 
                                        ]
                            ),
                            (os.path.join("pynnkit","MNIST", "archive", "train-images-idx3-ubyte"), 
                                        [
                                            os.path.join("pynnkit","MNIST", "archive", "train-images-idx3-ubyte", "train-images-idx3-ubyte"),
                                        ]
                            ),
                            (os.path.join("pynnkit","MNIST", "archive", "train-labels-idx1-ubyte"), 
                                        [
                                        os.path.join("pynnkit","MNIST", "archive", "train-labels-idx1-ubyte", "train-labels-idx1-ubyte")
                                        ]
                            ),
                ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy>=1.26.2"
    ]
)
