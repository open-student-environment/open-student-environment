""" Student models """

from abc import ABCMeta, abstractmethod

import numpy as np

from pymc import Exponential, Uniform


class WrongAssignment(Exception):
    pass


class Student(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, env=None):
        self.env = env
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

    def __init__(self, name, lam=None, env=None):
        super(PoissonStudent, self).__init__(name, env)
        if lam is not None:
            self.lam = lam
        else:
            self.lam = Uniform('lam_%s' % self.name, lower=0, upper=1)
        self.expT = Exponential('tau_%s' % self.name, self.lam)
        self.dt = []
        self.timestamps = []
        self.t = 0
        self.params = [self.lam, self.expT]

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
        if self.env is not None:
            self.env.statements[self.name].append(s)
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
                raise WrongAssignment('Statement with actor %s assigned to'
                                      ' %s' % (actor, name))
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
        tt = zip([0] + self.timestamps[:-1], self.timestamps)
        dt = [y - x for x, y in tt]
        self.dt = np.array(dt, dtype=float)
        self.expT = Exponential(
            'tau_%s' % self.name, self.lam, value=self.dt, observed=True)
        self.params.append(self.expT)
        return self
