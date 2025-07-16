FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -e "s/http:\/\/archive.ubuntu.com\/ubuntu\//http:\/\/ftp.nluug.nl\/os\/Linux\/distr\/ubuntu\//" -i /etc/apt/sources.list.d/ubuntu.sources
RUN sed -e "s/http:\/\/security.ubuntu.com\/ubuntu\//http:\/\/ftp.nluug.nl\/os\/Linux\/distr\/ubuntu\//" -i /etc/apt/sources.list.d/ubuntu.sources

# see: https://devguide.python.org/getting-started/setup-building/#build-dependencies
RUN apt-get update && \
    apt-get --no-install-recommends --yes install git git-lfs wget build-essential gdb lcov pkg-config \
      libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
      libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
      lzma lzma-dev tk-dev uuid-dev zlib1g-dev libzstd-dev ca-certificates

# Download and install Python 3.13.5
RUN wget https://www.python.org/ftp/python/3.13.5/Python-3.13.5.tgz && \
    tar -xzf Python-3.13.5.tgz && \
    cd Python-3.13.5 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.13.5 Python-3.13.5.tgz

# Set python3 and pip3 to point to Python 3.13.3
RUN ln -sf /usr/local/bin/python3.13 /usr/bin/python3 && \
    ln -sf /usr/local/bin/pip3.13 /usr/bin/pip3

WORKDIR /gentripy
COPY . .

RUN pip3 install --upgrade -r requirements.txt

CMD ["python3", "--version"]
