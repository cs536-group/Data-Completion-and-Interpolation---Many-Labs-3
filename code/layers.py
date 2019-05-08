import numpy as np
from funcs import Sigmoid, TanH, ReLu, MSE, CrossEntropy


class DenseLayer:

    def __init__(self, in_size, out_size, activation = ReLu(), loss_function = CrossEntropy()):
        self.in_size = in_size
        self.out_size = out_size
        self.W = np.random.randn(in_size, out_size) * np.sqrt(2.0 / in_size)  # He initialization
        self.bias = 1
        self.activation = activation
        self.loss_function = loss_function
        self.delta = np.zeros(self.in_size)
        self.out = None

    def __repr__(self):
        return 'dense layer: ({}, {})'.format(self.in_size, self.out_size)

    def __str__(self):
        return 'dense layer: ({}, {})'.format(self.in_size, self.out_size)

    def forward(self, input_data):
        self.out = self.activation(np.dot(input_data, self.W) + self.bias)
        return self.out

    def backward(self, learning_rate, loss):
        # print(loss.shape, self.W.T.shape, np.dot(self.W, loss).shape)
        self.delta = np.dot(loss, self.W.T) * self.activation.derivative(np.dot(self.out, self.W.T))
        self.W -= learning_rate * np.dot(self.out.T, loss) / (loss.shape[0])
        # for j in range(self.in_size):
        #     self.delta[j] = 0
        #     for k in range(self.out_size):
        #         print(j, k, self.W.shape, self.delta[j], self.out, self.W[k], self.W[j, k])
        #         self.delta[j] = self.delta[j] + loss[k] * self.activation.derivative(np.dot(self.out, self.W[k])) \
        #                         * self.W[j, k]
                # self.delta[j] = self.delta[j] + loss[k] * self.activation.derivative(np.dot(self.W[k], self.out)) * self.W[j, k]

        # W_new = np.zeros(self.W.shape)
        # for i in range(self.in_size):
        #     for j in range(self.out_size):
        #         # print(i, j, self.W.shape)
        #         W_new = self.W[i, j] - learning_rate * loss[j] * self.activation.derivative(np.dot(self.out, self.W[j])) * self.out[j]
        #         # W_new = self.W[i][j] - learning_rate * loss[j] * self.activation.derivative(np.dot(self.W[j], self.out)) * self.out[j]
        # self.W = W_new
        return self.delta
