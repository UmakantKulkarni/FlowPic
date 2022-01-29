FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt -y update

RUN apt -y upgrade

RUN apt -y install curl wget apache2-utils default-jre default-jdk wget git vim nano make g++ net-tools iproute2 libssl-dev tcpdump jq iputils-ping apt-transport-https nghttp2-client bash-completion xauth gcc autoconf libtool pkg-config sshpass python3 python3-setuptools python3-pip qt5-default

RUN install h2 numpy scipy pandas matplotlib scikit-learn gdown pyqt5 opencv-python

#RUN pip3 install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow_cpu-2.7.0-cp38-cp38-manylinux2010_x86_64.whl

WORKDIR /root/

CMD ["sh", "-c", "sleep infinity"]