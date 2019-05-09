import numpy as np
from layers import DenseLayer
from funcs import MSE, ReLu, CrossEntropy, Sigmoid
import pickle

class NN:

    def __init__(self, learning_rate=0.0001, loss_function=CrossEntropy()):
        self.layers = []
        self.layers.append(DenseLayer(261, 150, dropout=0.1, activation=ReLu()))
        self.layers.append(DenseLayer(150, 50, activation=ReLu()))
        self.layers.append(DenseLayer(50, 150, activation=ReLu()))
        self.layers.append(DenseLayer(150, 261, activation=Sigmoid()))
        self.loss_function = loss_function
        self.learning_rate = learning_rate

    def forward(self, x):
        input_data = x
        for layer in self.layers:
            input_data = layer.forward(input_data)
        return input_data

    def backward(self, learning_rate, loss):
        for layer in reversed(self.layers):
            loss = layer.backward(learning_rate, loss)

    def get_loss(self, prediction, y):
        return self.loss_function(prediction, y)

    def epoch(self, X, y, flag):
        loss_list = []
        for i in range(len(y)):
            prediction = self.forward(X[i:i+1])
            prediction *= flag[i:i+1]
            derivative, loss = self.get_loss(prediction, y[i:i+1])
            self.backward(self.learning_rate, derivative)
            loss_list.append(np.sum(loss))
        return loss_list

    def train(self, X, y):
        for epoch in range(1000):
            self.epoch(X, y)
        print(np.average(self.epoch(X, y)))

    def predict(self, x):
        input_data = x
        for layer in self.layers:
            input_data = layer.predict(input_data)
        return input_data

    def test(self, X, y, flag):
        loss_list = []
        for i in range(len(y)):
            prediction = self.predict(X[i:i+1])
            prediction *= flag[i:i+1]
            derivative, loss = self.get_loss(prediction, y[i:i+1])
            loss_list.append(np.sum(loss))
        return loss_list


def test():
    nn = NN()

    X = np.array(([2, 9], [1, 5], [3, 6], [0, 12], [12, 0], [5, 1], [9, 3]), dtype=float)
    y = np.array(([92], [86], [89], [100], [52], [58], [67]), dtype=float)

    X = X / np.amax(X, axis=0)
    y = y / 100.0

    nn.train(X, y)


def load_data_from_file(filename = '../data/splitedData.pkl'):
    ret = None
    with open(filename, 'rb') as f:
        ret = pickle.load(f)
    return ret


def load_data(filename = '../data/splitedData.pkl'):
    data = load_data_from_file(filename)
    flag_train = np.array(data[0])
    X_train = np.array(data[1])
    flag_dev = np.array(data[2])
    X_dev = np.array(data[3])
    flag_test = np.array(data[4])
    X_test = np.array(data[5])
    return flag_train, X_train, flag_dev, X_dev, flag_test, X_test


def shuffle_data(a, b):
    # Acquired from https://stackoverflow.com/questions/4601373/better-way-to-shuffle-two-numpy-arrays-in-unison
    assert len(a) == len(b)
    c = np.c_[a.reshape(len(a), -1), b.reshape(len(b), -1)]
    a2 = c[:, :a.size // len(a)].reshape(a.shape)
    b2 = c[:, a.size // len(a):].reshape(b.shape)
    return a2, b2


if __name__ == '__main__':
    np.random.seed(1145141919)

    # preprocess data
    flag_train, X_train, flag_dev, X_dev, flag_test, X_test = load_data()
    flag_train[:, -38:] = False
    flag_dev[:, -38:] = False
    flag_test[:, -38:] = False
    X_train *= flag_train
    X_dev *= flag_dev
    X_test *= flag_test

    # build model
    nn = NN(learning_rate=0.01, loss_function=CrossEntropy())

    # train
    max_epoch = 1000
    for epoch in range(max_epoch):
        X, flag = shuffle_data(X_train, flag_train)
        loss_train_list = nn.epoch(X, X, flag_train)
        print('Training epoch {}, training loss = {}'.format(epoch, np.average(loss_train_list)))
        # print(len(loss_train_list))
        if epoch % 10 == 0:
            loss_dev_list = nn.test(X_dev, X_dev, flag_dev)
            print('Testing loss = {}'.format(np.average(loss_dev_list)))
