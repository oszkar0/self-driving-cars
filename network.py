import numpy as np

class MutableNeuralNetwork:
    def __init__(self, layers):
        self.layers = layers

    def predict(self, input):
        output = input

        for layer in self.layers:
            output = layer.forward_propagate(output)
        
        return output
    
    def mutate(alpha=0.1):
        for layer in self.layers:
            layer.weights += (np.random.rand(*layer.weights.shape) - 0.5) * alpha
            layer.bias += (np.random.rand(*layer.weights.bias) - 0.5) * alpha


class FullyConnectedLayer():
    def __init__(self, input_size, output_size):
        #  create weights and bias matrices, initially with random values
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5

    def forward_propagate(self, input_data):
        self.input = input_data
        # calculate and return output Y = X*W + B
        self.output = input_data @ self.weights + self.bias
        return self.output