from pymc import Uniform, MCMC
from pylab import hist, show

from environment import Environment
from student import PoissonStudent


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
    params = [lam]
    for s in students:
        params.extend(s.params)
    m = MCMC(params)
    m.sample(iter=10000, burn=1000, thin=10)
    hist(m.trace('lambda_david')[:])
    show()


if __name__ == '__main__':
    main()
