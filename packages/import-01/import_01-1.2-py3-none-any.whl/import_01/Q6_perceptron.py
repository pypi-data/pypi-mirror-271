print("""
import numpy as np

def initialize_weights_and_bias(num_features):
    # Initialize weights with small random values and bias to 0
    weights = np.random.rand(num_features)
    bias = np.random.rand(1)
    return weights, bias

def perceptron_train(inputs, targets, weights, bias, learning_rate=0.1, max_iterations=1000):
    num_iterations = 0
    converged = False

    while not converged and num_iterations < max_iterations:
        num_iterations += 1
        converged = True

        for input_data, target in zip(inputs, targets):
            # Calculate the weighted sum
            weighted_sum = np.dot(weights, input_data) + bias[0]

            # Apply the step function
            output = 1 if weighted_sum >= 0 else 0

            # Update weights and bias if necessary
            if output != target:
                converged = False
                weights += learning_rate * (target - output) * input_data
                bias += learning_rate * (target - output) * 1  # Update bias

    return weights, bias, num_iterations

# Example usage:
# Assuming you have 'inputs' and 'targets' defined somewhere before this point
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
targets = np.array([0, 0, 0, 1])

# Initialize weights and bias
num_features = len(inputs[0])
weights, bias = initialize_weights_and_bias(num_features)

# Train the perceptron
trained_weights, trained_bias, num_iterations = perceptron_train(inputs, targets, weights, bias)

# Print the results
print(f"Converged in {num_iterations} iterations")
print("Trained Weights:", trained_weights)
print("Trained Bias:", trained_bias[0])


output -- 
Converged in 12 iterations
Trained Weights: [0.2657286  0.11677473]
Trained Bias: -0.30622280258733453

""")