
# rocket_relations
Rocket relations calculates characteristic velocity (c*), area_ratio, thrust
coefficient (C_F), specific impulse (ISP), exhaust velocity (ve), propellant mass flow (m_dot), and thrust (F_th, F) under standard assumptions of isentropic, steady, and choked flow.

## Installation
Download the source code or clone the repo locally.
In the project root directory, open a terminal and create/activate
a fresh conda environment (or reuse an existing one):
```
bash
conda create -n rocketenv python=3.10
conda activate rocketenv
pip install -e .

## Quickstart
At the top of your code, import the following parameters:
'''
from rocket_relations.ideal import c_star, thrust_coefficient, ve, Isp, m_dot, F_th, F
'''
Then define your input values
'''
T0 = ...
R = ...
gamma = ...
Pe = ...
Pa = ...
a_star
area_ratio = ....

'''

Then compute your desired parameter
## Help
help(rocket_relations.ideal.c_star)
help(rocket_relations.ideal.thrust_coefficient)
help(rocket_relations.ideal.area_ratio)
help(rocket_relations.ideal.Isp)
help(rocket_relations.ideal.ve)
help(rocket_relations.ideal.m_dot)
help(rocket_relations.ideal.F_th)
help(rocket_relations.ideal.F)
## Testing
To test the package, run "pytest -q". If passed, the following will show in green:

.....................                                                               [100%]
21 passed in 0.87s