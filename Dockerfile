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

## Create new user
RUN useradd kaggle -m -d /home/kaggle -s /bin/bash
RUN adduser kaggle sudo

# jupyter notebook
RUN mkdir -p /home/kaggle/analysis
RUN chown -R kaggle /home/kaggle

ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# user activation
EXPOSE 8888
RUN echo 'kaggle ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
USER kaggle

VOLUME /home/kaggle/analysis
WORKDIR /home/kaggle/analysis

CMD ["jupyter", "notebook", "--no-browser", "--ip=0.0.0.0", "--port=8888", "--notebook-dir='/home/kaggle/analysis'"]
