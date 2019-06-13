# HW3 Tester

NOTE: We are using Python 3. Make sure you are too:

```
(hw3) $ python --version
Python 3.6.1 :: Continuum Analytics, Inc.
```

## Installation:

You can run the testing script 3 different ways:

1. Conda:

```bash
# create conda environment and activate it
conda create -n hw3 python=3
source activate hw3

# install dependencies
conda install numpy pydot networkx progressbar2
pip install pymdptoolbox pygraphviz

# run the script to test the sample mdp
python hw3_tester.py -vvv -m sample.json -i
```

2. Pip:

```bash
pip3 install numpy pydot networkx progressbar2 pygraphviz pymdptoolbox
# or
pip3 install -r requirements.txt
```

### pygraphviz failing to install?
`pygraphviz` requires you to have the graphviz package installed on your OS.
See this [thread](https://github.com/rldm/hw3-tester/issues/2)

### Installing `pygraphviz` on Windows

*instructions inspired and adapted from [here](https://stackoverflow.com/questions/40809758/howto-install-pygraphviz-on-windows-10-64bit) and [here](https://stackoverflow.com/questions/45093811/installing-pygraphviz-on-windows-10-64-bit-python-3-6/54890705#54890705)*

* Download `graphviz-2.38.msi` (a dependency of `pygraphviz`) from here:
  * https://graphviz.gitlab.io/_pages/Download/Download_windows.html
  * Install it manually
  * Add `graphviz` tot PATH; specifically, add `C:\Program Files (x86)\Graphviz2.38\bin`
    * from the Windows menu (Windows logo key), search for: "*Environment Variables*" (the entry should be called "*Edit the system environment variables*")
    * click on Environment Variables
    * under `User variables for <username>`, find `Path` and double click on it
    * click `New`
    * add `C:\Program Files (x86)\Graphviz2.38\bin` and click `OK`
    * **restart the Anaconda window and other command prompt windows that are open**
    * *there is an easier way of doing this, through `SETX`, but it is dangerous as it can erase your entire `PATH` variable if you make some typos*
* Download the `pygraphviz` wheel from here:
  * **Python 3.5/3.6/3.7**
    * https://github.com/CristiFati/Prebuilt-Binaries/tree/master/Windows/PyGraphviz
  * **Python 2.7**
    * https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygraphviz
* Navigate to the directory where the downloaded wheel file is located
* Run `pip install your_downloaded_pygraphviz_file.whl`
  * Example for **Python 3.5 on Windows 10 amd64**: `pip install pygraphviz-1.5-cp35-cp35m-win_amd64.whl`
* Now you should have `pygraphviz` successfully installed. Test it properly by running the tester script with the `-s` flag.
  * `python hw3_tester.py -m sample.json -i -vvv -s`

Another possible solution has been offered [here](https://stackoverflow.com/questions/45093811/installing-pygraphviz-on-windows-10-64-bit-python-3-6/53137438#53137438) but I have not tested it.

1. Docker:

```bash
docker build -t rldm/hw3-tester:v1 .
docker run --privileged=true --rm \
    -v $PWD:/mnt/hw3-tester \
    -it rldm/hw3-tester:v1 /bin/bash
```

On windows using powershell:

```powershell
docker build -t rldm/hw3-tester:v1 .
$WorkingDir = Convert-Path .
docker run --privileged=true --rm -v $WorkingDir\:/mnt/hw3-tester -it rldm/hw3-tester:v1 /bin/bash
```

If you run into permissions errors when the docker container is building, you might have to change the Dockerfile to run the pip command before it resets the user back to the non root user.

If you run the test script in the next section and it gives you trouble about pymdptoolbox not being there, rerun the `pip` command inside the container without using `pip3`, use `pip` instead.

## Testing the script

```bash
python hw3_tester.py -m sample.json -i -vvv
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

