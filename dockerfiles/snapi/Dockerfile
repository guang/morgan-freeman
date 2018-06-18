FROM debian:jessie
MAINTAINER Guang Yang <garry.yangguang@gmail.com>

WORKDIR /home/dev
ENV HOME /home/dev

RUN apt-get update -y && apt-get install -y \
    wget \
    curl \
    net-tools \
    unzip \
    python \
    ruby \
    git \
    vim-nox \
    tcpdump \
    screen \
    ruby-dev \
    cmake \
    pkg-config \
    libffi-dev \
    libssl-dev \
    libmysqlclient-dev \
    libkrb5-dev \
    python-dev \
    python-psycopg2 \
    python-matplotlib \
    python-lxml \
    python-scipy \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Not the most updated pip cos im not hipster enough
RUN curl -s https://bootstrap.pypa.io/get-pip.py > get-pip.py \
 && python get-pip.py pip==7.1.2

ADD pip-requirements.txt /pip-requirements.txt
RUN pip install -r /pip-requirements.txt

# Start-up script
ADD clone_repos.sh /clone_repos.sh
RUN chmod +x /clone_repos.sh
