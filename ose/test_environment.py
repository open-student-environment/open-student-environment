import unittest
from .environment import Environment
from .student import PoissonStudent
from pymc import Uniform, MCMC


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
        self.assertGreaterEqual(statements[-1]["timestamp"], 8,
                                msg="The environment generated an unexpected"
                                    "low amount of data for a student")

    def test_environment(self):
        env = Environment(self.students, self.statements)
        self.assertEqual(len(env._statements.keys()),
                         3,
                         msg="The environment created a different"
                             " number of student than there is in"
                             " the statements")

    def test_add_student(self):
        env = Environment(self.students, self.statements)
        student = PoissonStudent(name='John', lam=2)
        env.add_student(student)
        self.assertEqual(len(env.students.keys()), 2,
                         msg="Adding a student didn't change the number of" +
                             "student in the environment")

    def test_statements_added_to_student(self):
        env = Environment(self.students, self.statements)
        student = PoissonStudent(name='John', lam=2)
        env.add_student(student)
        self.assertEqual(len(env.students[student.name].dt),
                         len(env._statements[
                                 student.name]),
                         msg="The student statements and dt have different "
                             "sizes")

    def test_fit(self):
        statement = {'actor': u'123456789-1234-1234-1234-12345678901234',
         'verb': u'http://adlnet.gov/expapi/verbs/completed',
         'timestamp': 1519862425.0}
        user_name = '123456789-1234-1234-1234-12345678901234'
        lam = Uniform('lam', lower=0, upper=1)
        s1 = PoissonStudent(user_name, lam=lam)
        env = Environment([s1], [statement])
        env.add_student(s1)
        res = env.fit([lam], method='mcmc')
        self.assertIsInstance(res, MCMC,
                              msg="The output of fit is not an PYMC instance")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testPoissonStudent']
    unittest.main()
