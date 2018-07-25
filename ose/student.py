""" Student models """

from abc import ABCMeta, abstractmethod
from scipy.stats import expon


class Student(object):

    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def study(self):
        pass


class PoissonStudent(Student):

    def __init__(self, lam):

        self.lam = lam
        self.dt = []
        self.t = 0

    def study(self):

        scale = 1 / self.lam
        tau = expon(scale=scale)
        self.dt.append(tau)
        self.t += tau.value
        s = {
            'actor': self.name,
            'verb': 'studied',
            'object': 'resource',
            'timestamp': self.t
        }
        return s
