from environment import Environment
from student import PoissonStudent

from pymc import 


STATEMENTS_PATH = "/Users/davidpanou/Documents/eig/Maskott/data.json"


def main():
    s1 = PoissonStudent("arnaud", 1)
    s2 = PoissonStudent("francois", 1)
    s3 = PoissonStudent("david", 0.5)

    students = [s1, s2, s3]
    env = Environment(students)
    statements = env.simulate(1000, verbose=True)

    student_names = set(s['actor'] for s in statements)
    lam = Normal('lam', mu=0, sigma=1)
    students = [PoissonStudent(name=name, lam=lam) for name in student_names]
    env = Environment(students, statements)
    env.fit()
    env.show()


def main2():
    env = Environment(None)
    env.load(STATEMENTS_PATH,PoissonStudent)
    print(len(env.students))

if __name__ == '__main__':
    main2()
