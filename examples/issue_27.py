from ose.statement import load_file, load_statements
from ose.utils import filter_by_users, graph2gephi, get_active_agents, \
    load_agent_data, get_structure
from ose.environment import Environment
from ose.student import PoissonStudent


def main():
    filename = 'data/statements-brneac3-20180301-20180531.json'
    statements = load_file(filename)
    statements = load_statements(statements)

    filename = '../data/accounts-brneac3-0-20180630.json'
    data = load_agent_data(filename)
    agent, adjancy = get_structure(data)
    active_agents = get_active_agents(statements)
    clean_agent, clean_stuct = filter_by_users(agent, adjancy, active_agents)

    students = [PoissonStudent(k, 1) for k, v in list(clean_agent.items())[:10]
                if v == 'user:eleve']

    env = Environment(agents=students,
                      statements=statements,
                      nodes=clean_agent,
                      structure=clean_stuct)

    env.plot_group_activity('0680111B')


if __name__ == '__main__':
    main()
