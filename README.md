[![CircleCI](https://circleci.com/gh/open-student-environment/open-student-environment.svg?style=shield&circle-token=03ce5e2996c8d68da81e8d82b00bd5965c542b45)](https://circleci.com/gh/open-student-environment/open-student-environment) [![codecov](https://codecov.io/gh/open-student-environment/open-student-environment/branch/master/graph/badge.svg)](https://codecov.io/gh/open-student-environment/open-student-environment)

# Open Student Environement

The Open Student Environment (OSE) is a framework to train models of students 
using xAPI statements.

# Installation

First install the dependencies with:
```
pip install numpy==1.11.0
pip install scipy==0.17.1
pip install -r requirements.txt
```

And then `pip install .` (or `pip install -e .` for development mode)

# Usage

OSE takes xAPI data as input and fit a model specified by the user using MCMC simulation, based on pymc.

A `model` is the specification of an agent and the variables that describe it the best.

`Variables` are random variables that follows distributions specified by the user, the goal is to find the parameters
of those distributions.

After describing the agent's behavior using random variables that depend on one another, the parameter are then computed using MCMC simulation.

# Example

```
from ose.statement import load_file, load_statements
from ose.utils import filter_by_users, graph2gephi, get_active_agents, load_agent_data, get_structure
from ose.environment import Environment
from ose.student import PoissonStudent
````
Library imports.
Here, the student activity is modeled by a Poisson distribution whose parameter `\lambda` have to be computed.

````

filename = 'data/statements-brneac3-20180301-20180531.json'
statements = load_file(filename)
statements = load_statements(statements)
````
The files contaning the xAPI data representing the students activity in a json file.

````
data = load_agent_data(filename)
agent, adjancy = get_structure(data)
students = [ PoissonStudent(k,1) for k,v in list(agent.items())[:10] if v == 'user:eleve']
````
It is possible to add extra data adding complementary information to the user's infos

````
env = Environment(agents=students,
                 statements=statements,
                 nodes=agent,
                 structure=adjancy)
res = env.fit([lam], method='mcmc')
print(res)
## plotting. can be integrated in env
hist(res.trace('lambda_{}'.format(user_name))[:])
show()                 
````
Fitting and plotting the expected values of `\lambda` parameters for every students.


# Visualization

Results can be visualized through [client interface](https://github.com/open-student-environment/ose-client).

# Testing

Run the following command:

```
pytest
```


