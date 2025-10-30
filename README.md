
# rocket_relations
Rocket relations calculates the thurst coefficient (thrust_coefficient) and characteristic velocity (c_star) of a rocket engine assume ideal rocket conditions.
## Installation
Download the source code or clone the repo locally.
In the project root directory, open a terminal and create/activate
a fresh conda environment (or reuse an existing one):
```
bash
conda create -n rocketenv python=3.14
conda activate rocketenv
pip install -e .
```
## Quickstart
At the top of your code, import the following parameters:
'''
import rocket_relations
import c_star
import thrust_coefficient
'''
Then define your input values
'''
T0 = ...
R = ...
gamma = ...
pe_p0 = ...
pa_p0 = ...
area_ratio = ....
'''

Then compute your thrust coefficient and characteristic velocity
## Help
help(rocket_relations.ideal.c_star)
help(rocket_relations.ideal.thrust_coefficient)
## Testing
To test the package, run "pytest -q". If passed, the following will show in green:

.....................                                                               [100%]
21 passed in 0.87s