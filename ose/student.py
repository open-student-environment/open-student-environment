""" Student models """

from abc import ABCMeta, abstractmethod
from functools import reduce
from pymc import Exponential


class Student(object):

    __metaclass__ = ABCMeta

    def __init__(self, name, env=None):
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

    def __init__(self, name, lam, env=None):
        super(PoissonStudent, self).__init__(name, env)
        self.expT = Exponential('lambda_%s' % self.name, lam)
        self.dt = []
        self.timestamps = []
        self.t = 0
        self.params = [self.expT]

    def study(self):
        """
        Generate an xAPI statement
        """
        tau = self.expT.random()
        self.dt.append(tau)
        self.t += tau
        s = {
            'actor': self.name,
            'verb': 'studied',
            'object': 'resource',
            'timestamp': self.t
        }
        if self.env is not None:
            self.env.statements.append(s)
        return s

    def _get_timestamps(self, statements):
        """
        Extract timestamps from xAPI statement

        Parameters
        ----------
        statements: list[Statement]
            The xAPI statements used to compute time intervals.

        Return
        ------
        timestamps: float
            A sorted list of timestamps
        """
        timestamps = []
        for statement in statements:
            actor, name = statement['actor'], self.name
            if actor != name:
                raise('Statement with actor %s assigned to %s' % (actor, name))
            timestamps.append(statement['timestamp'])
        return sorted(timestamps)

    def update(self, statements):
        """
        Updates the sample graph using the history of xAPI statements

        Parameters
        ----------
        statements: list[Statements]
            A list of xAPI statements

        Return
        ------
        self: PoissonStudent
            The current instance of a PoissonStudent
        """
        self.timestamps = self._get_timestamps(statements)
        self.dt = reduce((lambda x, y: y - x), self.timestamps)
        self.expT.value = self.dt
        self.expT.observed = True
        return self
