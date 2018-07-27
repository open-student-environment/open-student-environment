from environment import Environment
from student import PoissonStudent
from pymc import Uniform


def main():
    s1 = PoissonStudent("arnaud", 1)
    s2 = PoissonStudent("francois", 1)
    s3 = PoissonStudent("david", 0.5)

    students = [s1, s2, s3]
    env = Environment(students)
    statements = env.simulate(1000, verbose=True)

    student_names = set(s['actor'] for s in statements)
    lam = Uniform('lam', lower=0, upper=1)
    students = [PoissonStudent(name=name, lam=lam) for name in student_names]
    env = Environment(students, statements)
#     env.fit()
#     env.show()


if __name__ == '__main__':
    main()
