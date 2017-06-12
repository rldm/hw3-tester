# HW3 Tester

## Installation:

You can run the testing script 3 different ways:

1. Conda:

```bash
# create conda environment and activate it
conda create -n hw3 python=2
source activate hw3

# install dependencies
conda install numpy pydot networkx progressbar
pip install pymdptoolbox pygraphviz

# run the script to test the sample mdp
python hw3_tester.py -vvv -m sample.json -i -s
```

2. Pip:

```bash
pip3 install numpy pydot networkx progressbar2 pygraphviz pymdptoolbox
```

3. Docker:

```bash
docker build -t rldm/hw3-tester:v1 .
docker run --privileged=true --rm \
    -v $PWD:/mnt/hw3-tester \
    -it rldm/hw3-tester:v1 /bin/bash
```

## Testing the script

```bash
python hw3_tester.py -m sample.json -i -s -vvv
```

Output will show:

```
06/12/2017 01:57:32 AM - INFO: 
06/12/2017 01:57:32 AM - INFO: mdp returned median number of iterations 2
number of iterations: 2
06/12/2017 01:57:32 AM - INFO: end of script
```

An image will be created on the same directory the `json` file.

## Help?

```
python hw3_tester.py -h
usage: hw3_tester.py [-h] [-v] [-vv] [-vvv] -m MDP_PATH [-c] [-i] [-s]

Reinforcement Learning and Decision Making, HW3 Tester

optional arguments:
  -h, --help            show this help message and exit
  -v                    logging level set to ERROR
  -vv                   logging level set to INFO
  -vvv                  logging level set to DEBUG
  -m MDP_PATH, --mdp MDP_PATH
                        Path to the MDP json file
  -c, --check_only      Flag to only check valid MDP on JSON file
  -i, --iterations      Calculate how many iterations PI takes to solve this
  -s, --visualize       Visualize MDP (export to png)
```

