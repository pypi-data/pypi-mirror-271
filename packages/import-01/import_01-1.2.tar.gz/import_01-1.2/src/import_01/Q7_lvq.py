print(  """
  
  
import numpy as np
import matplotlib.pyplot as plt

class lvq:
    def __init__(self, input_size, output_size, learning_rate=0.1):
        self.input_size = input_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        self.weights = np.random.rand(output_size, input_size)

    def find_winner(self, data_point):
        distances = np.linalg.norm(self.weights - data_point, axis=1)
        winner_index = np.argmin(distances)
        return winner_index

    def update_weights(self, data_point, winner_index, target, learn_rate):
        self.weights[winner_index] += learn_rate * (data_point - self.weights[winner_index])

    def train(self, data, targets, prototypes, epochs=100):
        for epoch in range(epochs):
            for i in range(len(data)):
                data_point = data[i]
                target = targets[i]
                winner_index = self.find_winner(data_point)
                if target == prototypes[winner_index]:
                    self.update_weights(data_point, winner_index, target, self.learning_rate)

    def predict(self, data):
        predictions = []
        for data_point in data:
            winner_index = self.find_winner(data_point)
            predictions.append(winner_index)
        return np.array(predictions)

np.random.seed(42)
class_0 = np.random.rand(50, 2) * 0.5
class_1 = 0.5 + np.random.rand(50, 2) * 0.5
data = np.concatenate((class_0, class_1))
labels = np.concatenate((np.zeros(50), np.ones(50)))
prototypes = np.array([0, 1])  # Assign prototype targets for each output neuron

lvq_model = lvq(input_size=2, output_size=2, learning_rate=0.1)
lvq_model.train(data, labels, prototypes, epochs=1000)

test_data = np.random.rand(10, 2)
predictions = lvq_model.predict(test_data)

plt.scatter(class_0[:, 0], class_0[:, 1], color='blue', label='class0')
plt.scatter(class_1[:, 0], class_1[:, 1], color='red', label='class1')
plt.scatter(test_data[:, 0], test_data[:, 1], color='green', marker='*', label='testdata')
for i in range(lvq_model.output_size):
    plt.plot([lvq_model.weights[i, 0]], [lvq_model.weights[i, 1]], marker='o', markersize=10, color='black')
plt.title('LVQ Classes')
plt.legend()
plt.show()
  """)