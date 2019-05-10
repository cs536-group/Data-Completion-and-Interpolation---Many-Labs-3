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
        zeros = np.zeros(z.shape)
        return np.maximum(zeros, z)

    def derivative(self, z):
        zeros = np.zeros(z.shape)
        ones = np.ones(z.shape)
        ret = np.minimum(ones, z)
        ret = np.maximum(zeros, ret)
        return ret


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


class RMSE:
    def __call__(self, predict, y):
        """

        :param predict:
        :param y:
        :return: (derivative, loss)
        """
        diff = predict - y
        loss = np.abs(diff)
        return diff / loss, loss


class CrossEntropy:
    def __call__(self, predict, y):
        """

        :param predict:
        :param y:
        :return: (derivative, loss)
        """
        m = y.shape[0]
        y1 = y * np.log(predict)
        y0 = (1 - y) * np.log(1 - predict)
        # t = 0 * np.log(predict)
        loss = -1.0 / m * (y1 + y0)
        derivative = -1.0 / m * ((y - predict) / (predict - predict * predict))
        return derivative, loss


