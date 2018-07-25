""" Simulation environment """

from student import Student
import datetime
import numpy as np


class Environment(object):

    def __init__(self, student_list, max_time=None):
        """

        :param max_time:
        """
        self.student_list = student_list
        self.max_time = max_time

    def simulate(self, time_max=None, debug=False):
        """

        """
        res = []

        if time_max == None:
            time_max = self.max_time

        tmin = time_max - np.finfo(float).eps
        if debug:
            i = 0
            print(i)
        while (tmin <= time_max):
            for s in self.student_list:
                temp = s.study()
                tmin = min(temp['timestamp'], tmin)
                if temp["timestamp"] < time_max:
                    pass
            i = i +1
            if debug:
                print("iteration : {} \t\t timestamp_min : {}".format(i, tmin))
        return res
