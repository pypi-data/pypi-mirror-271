import os

# String holders for code
activation_function = """
import numpy as np
import matplotlib.pyplot as plt

def binary_step(x):
    return np.where(x >= 0, 1, 0)

def linear(x):
    return x
    
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return 2/(1 + np.exp(-2 * x)) -1

def relu(x):
    return np.maximum(0, x)

def leaky_relu(x, alpha=0.01):
    return np.maximum(alpha*x, x)

def elu(x, alpha=0.01):
    return np.where(x >= 0, x, alpha*(np.exp(x) - 1))

def swish(x):
    return x * sigmoid(x)

def plot_activation_function(function, name):
    x = np.linspace(-5, 5, 100)
    y = function(x)

    plt.plot(x, y, label=name)
    plt.legend()
    plt.title(f'{name} Activation Function')
    plt.xlabel('Input')
    plt.ylabel('Output')
    plt.grid(True)
    plt.show()

# Plotting activation functions
plot_activation_function(sigmoid, 'Sigmoid')
plot_activation_function(tanh, 'Tanh')
plot_activation_function(relu, 'ReLU')
plot_activation_function(leaky_relu, 'Leaky ReLU')
plot_activation_function(binary_step, 'Binary step')
plot_activation_function(elu, 'ELU')
plot_activation_function(linear, 'Linear')
plot_activation_function(swish, 'swish')
"""

mcculloh_pitt = """
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.linear_model import Perceptron
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPClassifier

class McCullochPittsNeuron:
    def __init__(self):
        pass

    def activate(self, inputs, weights, threshold=3):
        weighted_sum = sum(w * x for w, x in zip(weights, inputs))
        if weighted_sum >= threshold:
            return 1
        else:
            return 0
    
    def andnot(self, x1, x2, weights):
        inputs = np.array([x1, x2])
        return self.activate(inputs, weights) 

neuron = McCullochPittsNeuron()
weights = [1, 4]
x1 = 0; x2 = 0
output = neuron.andnot(x1, x2, weights)
print(output)
"""

ascii_perceptron = """ 
import numpy as np

class Perceptron:
    def __init__(self, input_size, learning_rate=0.1):
        # Initialize weights and bias
        self.weights = np.zeros(input_size)
        self.bias = 0
        self.learning_rate = learning_rate

    def predict(self, inputs):
        # Calculate the weighted sum
        weighted_sum = np.dot(self.weights, inputs) + self.bias
        # Return 1 if sum is greater than or equal to 0, otherwise 0
        return 1 if weighted_sum >= 0 else 0

    def train(self, inputs, label):
        # Get prediction
        prediction = self.predict(inputs)
        # Calculate error
        error = label - prediction
        # Update weights and bias based on error
        self.weights += self.learning_rate * error * inputs
        self.bias += self.learning_rate * error

# Training data
training_data = {
    "48": 1, "49": 0, "50": 1, "51": 0, "52": 1,
    "53": 0, "54": 1, "55": 0, "56": 1, "57": 0
}

# Initialize perceptron with 7 input nodes
perceptron = Perceptron(input_size=7)

# Train perceptron with training data
for ascii_code, label in training_data.items():
    inputs = np.array([int(b) for b in bin(int(ascii_code))[2:].zfill(7)])
    perceptron.train(inputs, label)

# Testing data
test_data = {
    "48": "even", "49": "odd", "50": "even", "51": "odd",
    "52": "even", "53": "odd", "54": "even", "55": "odd",
    "56": "even", "57": "odd"
}

# Test perceptron with test data
for ascii_code, expected_output in test_data.items():
    inputs = np.array([int(b) for b in bin(int(ascii_code))[2:].zfill(7)])
    output = perceptron.predict(inputs)
    # Print results
    print(f"'{chr(int(ascii_code))}' is {'even' if output == 1 else 'odd'}.")
"""

descision_region_perceptron = """ 
import numpy as np
import matplotlib.pyplot as plt

# Define the training data
X = np.array([[2, 4], [4, 3], [5, 6], [7, 2], [8, 5], [9, 4]])
y = np.array([0, 0, 0, 1, 1, 1])

# Initialize the weights and bias
w = np.zeros(X.shape[1])
b = 0

# Define the learning rate and number of epochs
learning_rate = 0.1
num_epochs = 10

# Implement the perceptron learning algorithm
for _ in range(num_epochs):
    for xi, yi in zip(X, y):
        # Compute the activation function and make predictions
        activation = np.dot(w, xi) + b
        prediction = 1 if activation >= 0 else 0

        # Update weights and bias
        w += learning_rate * (yi - prediction) * xi
        b += learning_rate * (yi - prediction)

# Visualize decision regions
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                     np.arange(y_min, y_max, 0.1))
Z = np.dot(np.c_[xx.ravel(), yy.ravel()], w) + b
Z = np.where(Z >= 0, 1, 0)
Z = Z.reshape(xx.shape)

# Plot decision regions
plt.contourf(xx, yy, Z, alpha=0.4)
plt.scatter(X[:, 0], X[:, 1], c=y, edgecolor='k')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Perceptron Learning Law')
plt.show()
"""

recognize_5x3_matrix = """ 
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.linear_model import Perceptron
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPClassifier

class PerceptronNN:
    def __init__(self, nn=10):
        self.nn = nn
        self.clf = MLPClassifier(hidden_layer_sizes=(self.nn,), random_state=42)
        self.train_data = {
            0: [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
            1: [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
            2: [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
            3: [[1, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [1, 1, 1]],
            4: [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
            5: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
            6: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
            7: [[1, 1, 1], [0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 0, 0]],
            8: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
            9: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]]
        }

    def train(self):
        # Create the training set
        training_data = self.train_data
        X_train = []
        y_train = []
        for digit, data in training_data.items():
            X_train.append(np.array(data).flatten())
            y_train.append(digit)

        # Convert training data to NumPy arrays
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        # print(X_train, y_train)

        # Train the MLP classifier
        self.clf.fit(X_train, y_train)

    def recognize(self, test_data):
        # Convert test data to NumPy array
        X_test = np.array(test_data)
        predictions = self.clf.predict(X_test)
        majority_vote = np.argmax(np.bincount(predictions))
        return majority_vote

recognizer = PerceptronNN(16)
recognizer.train()
# test_data = [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]]
test_data = [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]]
test_data = np.array([test_data]).flatten()
predictions = recognizer.recognize([test_data])
print(predictions)
"""

ann_forward_backward = """ 
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

class NeuralNetwork:
    def __init__(self, x, y):
        self.input = x
        self.output = y
        self.hidden_size = 4
        self.weights1 = np.random.randn(self.input.shape[1], self.hidden_size)
        self.weights2 = np.random.randn(self.hidden_size, 1)

    def feedforward(self):
        self.hidden = sigmoid(np.dot(self.input, self.weights1))
        self.predicted_output = sigmoid(np.dot(self.hidden, self.weights2))

    def backpropagate(self):
        output_error = self.output - self.predicted_output
        d_predicted_output = output_error * sigmoid_derivative(self.predicted_output)
        hidden_error = d_predicted_output.dot(self.weights2.T)
        d_hidden = hidden_error * sigmoid_derivative(self.hidden)
        self.weights1 += self.input.T.dot(d_hidden)
        self.weights2 += self.hidden.T.dot(d_predicted_output)

    def train(self, epochs):
        for _ in range(epochs):
            self.feedforward()
            self.backpropagate()

    def predict(self, x):
        hidden = sigmoid(np.dot(x, self.weights1))
        predicted_output = sigmoid(np.dot(hidden, self.weights2))
        return predicted_output

X = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
y = np.array([[0], [1], [1], [0]])

nn = NeuralNetwork(X, y)
nn.train(10000)

x_test = np.array([[0, 0, 0], [1, 0, 0]])
for x in x_test:
    print("Input:", x)
    print("Output:", nn.predict(x))
"""

xor_backprop = """ 
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

input_size, hidden_size, output_size = 2, 3, 1
np.random.seed(1)
weights1, weights2 = np.random.randn(input_size, hidden_size), np.random.randn(hidden_size, output_size)

learning_rate, num_iterations = 0.1, 450000

for i in range(num_iterations):
    hidden_layer_output = sigmoid(np.dot(X, weights1))
    predicted_output = sigmoid(np.dot(hidden_layer_output, weights2))
    
    error = y - predicted_output
    d_predicted_output = error * sigmoid_derivative(predicted_output)
    
    d_hidden_layer = d_predicted_output.dot(weights2.T) * sigmoid_derivative(hidden_layer_output)
    
    weights2 += hidden_layer_output.T.dot(d_predicted_output) * learning_rate
    weights1 += X.T.dot(d_hidden_layer) * learning_rate

predicted_output = np.where(predicted_output > 0.20, 1, 0)
print(predicted_output)
"""

art_network = """ 
import numpy as np

class ARTNetwork:
    def __init__(self, num_input, rho, vigilance):
        self.num_input = num_input
        self.rho = rho
        self.vigilance = vigilance
        self.weights = np.zeros((num_input,))

    def train(self, input_pattern):
        output = self._classify(input_pattern)
        if output is not None:
            self._update_weights(input_pattern)
            return output
        else:
            self._adjust_weights(input_pattern)
            return self.train(input_pattern)

    def _classify(self, input_pattern):
        input_norm = input_pattern / np.linalg.norm(input_pattern)
        output = np.dot(self.weights, input_norm)
        return output if output >= self.rho else None

    def _update_weights(self, input_pattern):
        self.weights += input_pattern

    def _adjust_weights(self, input_pattern):
        input_norm = input_pattern / np.linalg.norm(input_pattern)
        self.weights = np.maximum(self.weights, input_norm)

    def recall(self, input_pattern):
        return self._classify(input_pattern)

# Example usage
num_input = 5
rho = 0.5
vigilance = 0.8

network = ARTNetwork(num_input, rho, vigilance)

# Training
input_patterns = [
    np.array([1, 0, 0, 0, 1]),
    np.array([0, 1, 0, 0, 1]),
    np.array([0, 0, 1, 0, 1]),
]

for pattern in input_patterns:
    output = network.train(pattern)
    print(f"Trained pattern {pattern} classified as {output}")

# Recall
input_pattern = np.array([1, 1, 0, 0, 1])
output = network.recall(input_pattern)
print(f"Recalled pattern {input_pattern} classified as {output}")
"""

hopfield_network = """ 
import numpy as np

class HopfieldNetwork:
    def __init__(self, num_neurons):
        self.num_neurons = num_neurons
        self.weights = np.zeros((num_neurons, num_neurons))

    def train(self, patterns):
        for pattern in patterns:
            self.weights += np.outer(pattern, pattern)
            np.fill_diagonal(self.weights, 0)

    def recall(self, pattern, max_iterations=100):
        iterations = 0
        while iterations < max_iterations:
            output = np.sign(np.dot(pattern, self.weights))
            if np.array_equal(pattern, output):
                break
            pattern = output
            iterations += 1
        return pattern

# Example usage
patterns = np.array([
    [-1, 1, 1, 1],
    [1, -1, 1, -1],
    [-1, -1, 1, 1],
    [-1, 1, -1, -1]
])

hopfield = HopfieldNetwork(num_neurons=4)
hopfield.train(patterns)

test_patterns = np.array([
    [-1, 1, 1, 1],
    [1, 1, -1, -1],
    [1, -1, -1, -1]
])

print("Stored Patterns:")
for i, pattern in enumerate(patterns):
    print(f"Pattern {i + 1}: {pattern}")

print("\nRecalled Patterns:")
for pattern in test_patterns:
    recalled_pattern = hopfield.recall(pattern)
    print(f"Input Pattern: {pattern}, Recalled Pattern: {recalled_pattern.flatten()}")
"""



cnn_object_detection = """ 
import tensorflow as tf
model = tf.keras.applications.MobileNetV2(weights='imagenet')
# Load image and preprocess it
image = tf.keras.preprocessing.image.load_img('download.jpeg', target_size=(224, 224))
image = tf.keras.preprocessing.image.img_to_array(image)
image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
image = tf.expand_dims(image, axis=0)
# Run object detection
predictions = model.predict(image)
decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions)
# Print top predicted objects
for _, label, confidence in decoded_predictions[0]:
    print(f"{label}: {confidence * 100}%")
"""

cnn_image_classification = """ 
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# Load and preprocess the dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
y_train, y_test = keras.utils.to_categorical(y_train, num_classes=10), keras.utils.to_categorical(y_test, num_classes=10)

# Define and compile the model
model = keras.models.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(32, 32, 3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model and get the training history
history = model.fit(x_train, y_train, batch_size=64, epochs=4, validation_data=(x_test, y_test))

# Evaluate the model
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print(f'Test Loss: {test_loss}\nTest Accuracy: {test_accuracy}')

# Plot training and validation accuracy
plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Validation')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Plot training and validation loss
plt.plot(history.history['loss'], label='Train')
plt.plot(history.history['val_loss'], label='Validation')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()
"""

cnn_tf_implementation = """
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.linear_model import Perceptron
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPClassifier

class CNNModel:
    def __init__(self, num_classes):
        self.num_classes = num_classes
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(self.num_classes, activation='softmax')
        ])
        return model

    def train(self, X_train, y_train, epochs=10, batch_size=128):
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

    def evaluate(self, X_test, y_test):
        loss, accuracy = self.model.evaluate(X_test, y_test)
        print("Test Loss:", loss)
        print("Test Accuracy:", accuracy)

    def predict(self, X):
        return self.model.predict(X)

(X_train, y_train), (X_test, y_test) = tf.keras.datasets.cifar10.load_data()

X_train = X_train / 255.0
X_test = X_test / 255.0

num_classes = 10
cnn_model = CNNModel(num_classes)
cnn_model.train(X_train, y_train, epochs=10, batch_size=32)
cnn_model.evaluate(X_test, y_test)
predictions = cnn_model.predict(X_test)
"""

mnist_detection = """ 
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.linear_model import Perceptron
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPClassifier

class MNISTClassifier:
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        return model

    def train(self, X_train, y_train, epochs=10, batch_size=32):
        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
    
    def visualize_data(self, X_data, y_data, num_samples=5):
        fig, axes = plt.subplots(1, num_samples, figsize=(10, 4))

        for i in range(num_samples):
            axes[i].imshow(X_data[i], cmap='gray')
            axes[i].set_title(f"Label: {y_data[i]}")
            axes[i].axis('off')

        plt.show()

    def evaluate(self, X_test, y_test):
        loss, accuracy = self.model.evaluate(X_test, y_test)
        print("Test Loss:", loss)
        print("Test Accuracy:", accuracy)

# Load the MNIST dataset
mnist = tf.keras.datasets.mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Preprocess the data
X_train = X_train / 255.0
X_test = X_test / 255.0

# Create an instance of the MNISTClassifier
mnist_classifier = MNISTClassifier()

# Train the model
mnist_classifier.train(X_train, y_train, epochs=10, batch_size=32)

# Evaluate the model
mnist_classifier.evaluate(X_test, y_test)

# To visualize the data
mnist_classifier.visualize_data( X_test, y_test, num_samples=5)
"""

bam = """ 
import numpy as np
def bam(input_patterns,output_patterns):
    input_patterns=np.array(input_patterns)
    output_patterns= np.array(output_patterns)
    weight_matrix = np.dot(output_patterns.T,input_patterns)
    def activation(input_pattern):
        output_pattern = np.dot(weight_matrix,input_pattern)
        output_pattern[output_pattern>=0]=1
        output_pattern[output_pattern<0]=-1
        return output_pattern    
    print("input patterns | output patterns")
    for i in range(input_patterns.shape[0]):
        input_pattern = input_patterns[i]
        output_pattern = activation(input_pattern)
        print(f"{input_pattern} | {output_pattern}")
input_patterns=[[1,-1,1,-1],[1,1,-1,-1]]
output_patterns=[[1,1],[-1,-1]]
bam(input_patterns,output_patterns)
"""


masterDict = {
    'activation_function' : activation_function,
    'mcculloh_pitt': mcculloh_pitt,
    'ascii_perceptron': ascii_perceptron,
    'descision_region_perceptron': descision_region_perceptron,
    'recognize_5x3_matrix': recognize_5x3_matrix,
    'ann_forward_backward': ann_forward_backward,
    'xor_backprop': xor_backprop,
    'art_network': art_network,
    'hopfield_network':hopfield_network,
    'cnn_object_detection': cnn_object_detection,
    'cnn_image_classification': cnn_image_classification,
    'cnn_tf_implementation': cnn_tf_implementation,
    'mnist_detection': mnist_detection,
    'bam': bam
}

class Writer:
    def __init__(self, filename):
        self.filename = os.path.join(os.getcwd(), filename)
        self.masterDict = masterDict
        self.questions = list(masterDict.keys())

    def getCode(self, input_string):
        input_string = self.masterDict[input_string]
        with open(self.filename, 'w') as file:
            file.write(input_string)
        print(f'##############################################')

if __name__ == '__main__':
    write = Writer('output.txt')
    # print(write.questions)
    write.getCode('descision_region_perceptron')