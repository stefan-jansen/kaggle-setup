#!/usr/bin/env bash

FROM ubuntu:16.04

ENV TERM=xterm
ENV LC_ALL=C

# Ubuntu package update & installation
RUN apt-get update -y
COPY dependencies.txt /tmp
RUN xargs -a /tmp/dependencies.txt apt-get build-dep -y
COPY packages.txt /tmp
RUN xargs -a /tmp/packages.txt apt-get install -y

# Python setup
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
#RUN pip3 install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.8.0-cp34-cp34m-linux_x86_64.whl

## Create new user
RUN useradd kaggle -d /home/kaggle -s /bin/bash
RUN adduser kaggle sudo

# jupyter notebook
COPY jupyter_notebook.sh /home/kaggle
RUN chown -R kaggle /home/kaggle
#RUN chmod 777 /home/kaggle/jupyter_notebook.sh

# user activation
EXPOSE 8888
RUN usermod -a -G sudo kaggle
RUN echo 'kaggle ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
COPY .bashrc.template /home/kaggle/.bashrc
USER kaggle

ENV SHELL=/bin/bash
ENV HOME=/home/kaggle
ENV USER=kaggle

RUN mkdir -p /home/kaggle/analysis

VOLUME /home/kaggle/analysis
WORKDIR /home/kaggle/analysis

CMD ['/home/kaggle/jupyter_notebook.sh']
