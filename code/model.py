import numpy as np
from layers import DenseLayer
from funcs import MSE, ReLu, CrossEntropy, Sigmoid


class NN:
    def __init__(self, learning_rate=0.004, loss_function=CrossEntropy()):
        self.layers = []
        self.layers.append(DenseLayer(2, 3, activation=ReLu()))
        self.layers.append(DenseLayer(3, 1, activation=Sigmoid()))
        self.loss_function = loss_function
        self.learning_rate = learning_rate

    def forward(self, X):
        input_data = X
        for layer in self.layers:
            input_data = layer.forward(input_data)
        return input_data

    def backward(self, learning_rate, loss):
        for layer in reversed(self.layers):
            loss = layer.backward(learning_rate, loss)
    #
    # def update_weights(self, loss):
    #     for layer in self.layers:
    #         layer.update_weights(loss)

    def epoch(self, X, y):
        loss_list = []
        for i in range(len(y)):
            prediction = self.forward(X[i:i+1])
            derivative, loss = self.loss_function(prediction, y[i:i+1])
            # print(derivative, loss)
            self.backward(self.learning_rate, derivative)
            loss_list.append(loss)
        print(np.average(loss_list))

    def train(self, X, y):
        for epoch in range(10):
            self.epoch(X, y)

def test():
    # a = np.array([[-1], [3], [-2], [4]])
    # print(ReLu().derivative(a))

    nn = NN()

    X = np.array(([2, 9], [1, 5], [3, 6], [0, 12], [12, 0], [5, 1], [9, 3]), dtype=float)
    y = np.array(([92], [86], [89], [100], [52], [58], [67]), dtype=float)

    # scale units
    X = X / np.amax(X, axis=0)  # maximum of X array
    y = y / 100  # max test score is 100

    nn.train(X, y)


if __name__ == '__main__':
    np.random.seed(1145141919)
    test()
