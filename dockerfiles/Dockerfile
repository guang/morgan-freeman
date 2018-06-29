FROM tensorflow/tensorflow:1.8.0-gpu
MAINTAINER Guang Yang <garry.yangguang@gmail.com>

RUN apt-get update -y && apt-get install -y \
    wget \
    sox \
    libsndfile1-dev \
    git \
    curl \
    net-tools \
    ffmpeg \
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
    awscli \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


ADD pip-requirements.txt /pip-requirements.txt
RUN pip install -r /pip-requirements.txt

# Add deep-voice-conversion

# Start-up script
ADD startup_script.sh /startup_script.sh
RUN chmod +x /startup_script.sh
