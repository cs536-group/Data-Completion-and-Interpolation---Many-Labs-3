import numpy as np


class Sigmoid:
    def __call__(self, z):
        return 1.0 / (1 + np.exp(-z))

    def derivative(self, z):
        return self.__call__(z) * (1 - self.__call__(z))
        #return sz * (1 - sz)


class TanH:
    def __call__(self, z):
        ez = np.exp(z)
        enz = np.exp(-z)
        return (ez - enz) / (ez + enz)

    def derivative(self, z):
        return 1 - np.square(self.__call__(z))


class ReLu:
    def __call__(self, z):
        return max(0, z)

    def derivative(self, z):
        if z < 0:
            return 0
        else:
            return 1


class Softmax:
    def __call__(self, z):
        ex = np.exp(x - np.max(x))
        return ex / ex.sum(axis = 0)

    def derivative(self, z):
        sm = self.__call__(z)
        sm = sm.reshape(-1, 1)
        return np.diagflat(sm) - np.dot(sm, sm.T)


class MSE:
    def __call__(self, predict, y):
        """

        :param predict:
        :param y:
        :return: (derivative, loss)
        """
        diff = predict - y
        return 2 * diff, np.square(diff)


class CrossEntropy:
    def __call__(self, predict, y):
        return

