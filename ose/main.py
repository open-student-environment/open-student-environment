from pymc import Uniform, MCMC, Model
from pylab import hist, show

from environment import Environment
from student import PoissonStudent


def main():
    s1 = PoissonStudent("arnaud", .3)
    s2 = PoissonStudent("francois", .3)
    s3 = PoissonStudent("david", .2)

    students = [s1, s2, s3]
    env = Environment(students)
    statements = env.simulate(1000, verbose=True)

    student_names = set(s['actor'] for s in statements)
    students = [PoissonStudent(name=name) for name in student_names]
    env = Environment(students, statements)
    params = []
    for s in students:
        params.extend(s.params)
    m = Model(params)
    sampler = MCMC(m)
    sampler.sample(iter=10000, burn=1000, thin=10)
    hist(sampler.trace('lam_arnaud')[:])
    show()


if __name__ == '__main__':
    main()
