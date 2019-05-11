import numpy as np
from funcs import Sigmoid, TanH, ReLu, MSE, CrossEntropy


class DenseLayer:

    def __init__(self, in_size, out_size, dropout=0, activation=ReLu(), loss_function=CrossEntropy()):
        self.in_size = in_size
        self.out_size = out_size
        self.W = np.random.randn(in_size, out_size) * np.sqrt(2.0 / in_size)  # He initialization
        self.bias = np.random.randn(1, out_size) * np.sqrt(2.0 / in_size)  # He initialization
        self.activation = activation
        self.loss_function = loss_function
        self.delta = np.zeros(self.in_size)
        self.out = None
        self.z = None
        self.input_data = None
        self.dropout = dropout
        self.mask = None

    def __repr__(self):
        return 'dense layer: ({}, {})'.format(self.in_size, self.out_size)

    def __str__(self):
        return 'dense layer: ({}, {})'.format(self.in_size, self.out_size)

    def predict(self, input_data):
        return self.activation(np.dot(input_data, self.W) + self.bias)

    def forward(self, input_data, dropout=True):
        # print('input_data shape: {}, self.W shape: {}'.format(input_data.shape, self.W.shape))
        self.input_data = input_data
        if dropout:
            self.mask = np.random.binomial(1, 1 - self.dropout, size=(1, self.in_size))
            # print(self.mask)
            self.input_data = self.input_data * self.mask
        # print(self, self.input_data, self.mask, self.W)
        self.z = np.dot(self.input_data, self.W) + self.bias
        self.out = self.activation(self.z)
        # print('{} {} {}'.format(input_data, self.W, self.out))
        return self.out

    def backward(self, learning_rate, loss):
        # print(loss.shape, self.W.T.shape, np.dot(self.W, loss).shape)
        # print(self.out.shape)
        # print('loss.shape {} z.shape {}, w.shape {}'.format(loss.shape, self.z.shape, self.W.shape))
        # if loss.shape == (1, 1):
        #     loss = loss.item()
        # self.delta = loss * self.activation.derivative(self.z) * self.W.T
        # print(loss, self.delta)
        # print('out.shape {} delta.shape {}'.format(self.out.shape, self.delta.shape))
        # print((learning_rate * loss * self.out).shape)

        # self.z = np.dot(self.out, self.W.T) + self.bias
        # self.delta = (loss @ self.W.T) * self.activation.derivative(self.z)
        # self.W -= ((learning_rate * loss * self.out).T @ self.activation.derivative(self.z)).T

        # self.W2 = np.copy(self.W)
        self.delta = (loss * self.activation.derivative(self.z)) @ self.W.T
        self.W -= self.input_data.T @ (learning_rate * loss * self.activation.derivative(self.z))
        self.bias -= learning_rate * loss * self.activation.derivative(self.z)
        # self.delta2 = np.zeros(self.delta.shape)


        # for j in range(self.in_size):
        #     for k in range(self.out_size):
        #         print(j, k)
        #         self.delta2[0, j] += loss[0, k] * self.activation.derivative(self.z[0, k]) * self.W[j, k]

        # for i in range(self.in_size):
        #     for j in range(self.out_size):
        #         self.W2[i, j] -= learning_rate * loss[0, j] * self.activation.derivative(self.z[0, j]) * self.input_data[0, i]
        # print(self.delta, self.delta2)
        # print(self.W, self.W2)
        return self.delta
