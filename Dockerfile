FROM jupyter/scipy-notebook
MAINTAINER Miguel Morales <mimoralea@gmail.com>
USER root

# update ubuntu installation
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get upgrade -y

# install dependencies
RUN apt-get install -y python3 ipython3 python3-pip python3-dev
RUN apt-get install -y libgraphviz-dev graphviz python-pygraphviz
RUN apt-get install -y pkg-config

# clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# switch back to user
USER $NB_USER

# install necessary packages
RUN pip3 install --upgrade pip && pip3 install numpy pydot networkx progressbar2 pymdptoolbox pygraphviz

# make the dir with notebooks the working dir
WORKDIR /mnt/hw3-tester