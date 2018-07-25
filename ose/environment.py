""" Simulation environment """
import logging

logger = logging.getLogger(__name__)


class Environment(object):

    def __init__(self, students):
        """
        A Class for modeling the environment.

        Parameters
        ----------

        students: list[Student]
            A list of students
        """

        self.students = students

    def simulate(self, tmax, verbose=False):
        """
        Simulate the interaction of students with resources

        Parameters
        ----------
        tmax: float
            End time for the simulation
        """
        res = []
        tmin = 0
        while(tmin < tmax):
            tmin = tmax
            for s in self.students:
                statement = s.study()
                t = statement['timestamp']
                tmin = min(t, tmin)
                if t < tmax:
                    res.append(statement)
                    if verbose:
                        print("statement: {}".format(statement))
        return res
