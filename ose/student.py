""" Student models """

from abc import ABCMeta, abstractmethod


class Student(object):

    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def study(self):
        pass


class PoissonStudent(Student):

    def __init__(self, l):

        self.l = l
        self.t = 0
