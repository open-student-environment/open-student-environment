from environment import Environment
from student import PoissonStudent



def main():

    ps1 = PoissonStudent("arnaud",0.1)
    ps2 = PoissonStudent("francois", 1)
    ps3 = PoissonStudent("david", 0.5)

    student_list = [ps1,ps2,ps3]

    env = Environment(student_list,0.5)

    res = env.simulate(1000,debug=True)

    print(res)




if __name__ == '__main__':
    main()