""" Simulation environment """

import json
from collections import defaultdict
import functools

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

    def load(self, statements_file, student_builder):
        """
        Load a given dataset in memory and create the students.
        If students have been given at environment creation,
        they will be deleted before creating the new ones.
        In this version, all students are initialized at 1

        Parameters
        ---------
        statements : JSON file contains xAPI statements

        student_builder : Student
                 A method that specifies the logic in which
                 student are generated.
        """
        student_name = None
        student_hash = defaultdict(functools.partial(student_builder,student_name,1))
        statements = json.load(open(statements_file,"r"))

        for s in statements :
            current_statement = self.extract_information(s)
            student_name = current_statement.pop("name")
            student_hash[student_name].add(current_statement)

        self.students  = list(student_hash.values())


    @staticmethod
    def extract_information(statement):
        res = {"name": eval(statement["actor"])["account"]["name"],
               "verb": eval(statement["verb"])["display"],
               "timestamp": statement["timestamp"]}
        return res









