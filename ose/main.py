from .environment import Environment
from .student import PoissonStudent


def main():
    s1 = PoissonStudent("arnaud", 1)
    s2 = PoissonStudent("francois", 1)
    s3 = PoissonStudent("david", 0.5)

    students = [s1, s2, s3]
    env = Environment(students)
    res = env.simulate(1000, debug=True)

    print(res)

if __name__ == '__main__':
    main()
