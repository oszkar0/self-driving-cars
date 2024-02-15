import numpy as np

class MutableNeuralNetwork:
    def __init__(self, layers):
        self.layers = layers

    def predict(self, input):
        output = input

        for layer in self.layers:
            output = layer.forward_propagate(output)
        
        return output
    
    def mutate(self, alpha=0.1):
        mutated_layers = []

        for layer in self.layers:
            weights = layer.weights.copy() + (np.random.rand(*layer.weights.shape) - 0.5) * alpha
            bias = layer.bias.copy() + (np.random.rand(*layer.bias.shape) - 0.5) * alpha
            mutated_layer = FullyConnectedLayer(weights=weights, bias=bias)
            mutated_layers.append(mutated_layer)

        return MutableNeuralNetwork(mutated_layers)

class FullyConnectedLayer():
    def __init__(self, input_size=None, output_size=None, weights=None, bias=None):
        if weights is not None and bias is not None:
            self.weights = weights
            self.bias = bias
        elif input_size is not None and output_size is not None:
            #  create weights and bias matrices, initially with random values
            self.weights = np.random.rand(input_size, output_size) - 0.5
            self.bias = np.random.rand(1, output_size) - 0.5

    def forward_propagate(self, input_data):
        self.input = input_data
        # calculate and return output Y = X*W + B
        self.output = input_data @ self.weights + self.bias
        return self.output