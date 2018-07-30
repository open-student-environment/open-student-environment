import unittest
from .environment import Environment
from .student import PoissonStudent


class Test(unittest.TestCase):

    def setUp(self):
        self.students = [PoissonStudent(name='Ed', lam=2)]
        self.statements = [
            {'timestamp': 0.7354156191538802, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 0.8781497209426028, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.144202469575485, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.427249032536914, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.5319657470218193, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied', \
             'actor': 'John', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied', \
             'actor': 'John', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied', \
             'actor': 'Kevin', 'object': 'resource'}
        ]

    def tearDown(self):
        pass

    def test_simulate(self):
        env = Environment(self.students)
        statements = env.simulate(10)
        self.assertGreaterEqual(statements[-1]["timestamp"], 9,
                                msg="The environment generated an unexpected"
                                    + "low amount of data for a student")

    def test_environment(self):
        env = Environment(self.students, self.statements)
        self.assertEqual(len(env.statements.keys()),
                         3,
                         "The environment created a different"
                         + " number of student than there is in"
                         + " the statements")

    def test_add_student(self):
        env = Environment(self.students, self.statements)
        student = PoissonStudent(name='John', lam=2)
        env.add_student(student)
        self.assertEqual(len(env.students.keys()), 2,
                         "Adding a student didn't change the number of"
                         "student in the environment")

    def test_load_json(self):
        pass

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testPoissonStudent']
    unittest.main()
