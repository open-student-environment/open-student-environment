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

    def __init__(self, name, lam):

        self.name = name
        scale = 1 / lam
        self.expT = expon(scale=scale)
        self.dt = []
        self.t = 0

    def study(self):

        tau = self.expT.rvs()
        self.dt.append(tau)
        self.t += tau
        s = {
            'actor': self.name,
            'verb': 'studied',
            'object': 'resource',
            'timestamp': self.t
        }
        return s
