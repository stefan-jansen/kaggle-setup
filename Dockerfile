#!/usr/bin/env bash

FROM ubuntu:16.04

RUN apt-get update -y && apt-get install build-essential -y
COPY packages.txt /tmp
RUN xargs -a /tmp/packages.txt apt-get install -y

ENV TERM=xterm
ENV LC_ALL=C

# Python setup
RUN pip3 install virtualenv
RUN /usr/local/bin/virtualenv /opt/kaggle --distribute

COPY requirements.txt /tmp
RUN /opt/kaggle/bin/pip install -r /tmp/requirements.txt

## Create new user
RUN useradd kaggle -d /home/kaggle -s /bin/bash
RUN adduser kaggle sudo
RUN chown -R kaggle /opt/kaggle

# ipython
COPY ipython_nb.sh /home/kaggle
RUN chmod +x /home/kaggle/ipython_nb.sh
RUN chown -R kaggle /home/kaggle

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

CMD ['/home/kaggle/ipython_nb.sh']
