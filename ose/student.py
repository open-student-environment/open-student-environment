""" Student models """

from abc import ABCMeta, abstractmethod
from functools import reduce
from pymc import Exponential



class Student(object):

    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def study(self):
        pass


class PoissonStudent(Student):
    """
    Student model that generates activity according to a Poisson distribution.

    Parameters
    ----------
    name: str
        The name of the student
    lam: float or pymc.Distribution
        `lambda` parameter for the Poisson distribution
    """

    def __init__(self, name, lam):

        self.name = name
        self.expT = Exponential('lambda_%s' % self.name, lam)
        self.dt = []
        self.timestamps = []
        self.t = 0
        self.params = [self.expT]

    def study(self):

        tau = self.expT.random()
        self.dt.append(tau)
        self.t += tau
        s = {
            'actor': self.name,
            'verb': 'studied',
            'object': 'resource',
            'timestamp': self.t
        }
        return s

    def add(self, statement):
        """
        Add the xAPI statement the history of the student.

        Parameters
        ----------
        statement: Statement
            The xAPI statement to add to the model
        """
        actor, name = statement['actor'], self.name
        if actor != name:
            raise('Statement with actor %s assigned to %s' % (actor, name))
        self.timestamps.append(statement['timestamp'])

    def fit(self):
        """
        Builds a Bayesian Network from the history of xAPI statements
        """
        self.timestamps = sorted(self.timestamps)
        self.dt = reduce((lambda x, y: y - x), self.timestamps)
        self.expT = self.dt
        self.expT.observed = True
