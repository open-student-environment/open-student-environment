from environment import Environment
from student import PoissonStudent


STATEMENTS_PATH = "/Users/davidpanou/Documents/eig/Maskott/data.json"


def main():
    s1 = PoissonStudent("arnaud", 1)
    s2 = PoissonStudent("francois", 1)
    s3 = PoissonStudent("david", 0.5)

    students = [s1, s2, s3]
    env = Environment(students)
    res = env.simulate(1000, verbose=True)


def main2():
    env = Environment(None)
    env.load(STATEMENTS_PATH,PoissonStudent)
    print(len(env.students))
    print(list(map(lambda x : x.timestamps,env.students[1])))


if __name__ == '__main__':
    main2()
