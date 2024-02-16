import numpy as np

class MutableNeuralNetwork:
    def __init__(self, layers):
        self.layers = layers

    def predict(self, input):
        output = input

        for layer in self.layers:
            output = layer.forward_propagate(output)
        
        return output
    
    def mutate(self, mutation_rate=0.1):
        mutated_layers = []
        
        for layer in self.layers:
            mutated_weights = layer.weights.copy()
            mutated_bias = layer.bias.copy()
            
            # weights mutation
            for i in range(len(mutated_weights)):
                for j in range(len(mutated_weights[i])):
                    if np.random.rand() < mutation_rate:
                        mutated_weights[i][j] += np.random.uniform(-0.1, 0.1)  # Adjust mutation range as needed
            # bias mutation
            for i in range(len(mutated_bias)):
                if np.random.rand() < mutation_rate:
                    mutated_bias[i] += np.random.uniform(-0.1, 0.1)  # Adjust mutation range as needed
            
            mutated_layer = FullyConnectedLayer(weights=mutated_weights, bias=mutated_bias, activation_function=layer.activation_function)
            mutated_layers.append(mutated_layer)
        
        return MutableNeuralNetwork(mutated_layers)
    
class FullyConnectedLayer():
    def __init__(self, input_size=None, output_size=None, weights=None, bias=None, activation_function=None):
        if weights is not None and bias is not None:
            self.weights = weights
            self.bias = bias
        elif input_size is not None and output_size is not None:
            #  create weights and bias matrices, initially with random values
            self.weights = np.random.rand(input_size, output_size) * 2 - 1
            self.bias = np.random.rand(1, output_size) * 2 - 1

        self.activation_function = activation_function

    def forward_propagate(self, input_data):
        self.input = input_data
        # calculate and return output Y = X*W + B
        self.output = input_data @ self.weights + self.bias
        if self.activation_function is not None:
            self.output = self.activation_function(self.output)

        return self.output
    

## activation functions
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)