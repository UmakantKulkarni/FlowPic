#!/usr/bin/bash

apt-get update && apt-get -y upgrade && apt-get update

apt -y install curl wget apache2-utils default-jre default-jdk wget git vim nano make g++ net-tools iproute2 libssl-dev tcpdump jq iputils-ping apt-transport-https nghttp2-client bash-completion xauth gcc autoconf libtool pkg-config sshpass python3 python3-setuptools python3-pip qt5-default x11-apps feh

export CONDA_ALWAYS_YES="true"

cd /mydata && git clone https://github.com/UmakantKulkarni/scripts

wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-Linux-ppc64le.sh -O miniconda.sh

bash miniconda.sh -b -p /mydata/miniconda3

rm miniconda.sh
echo 'PATH="/mydata/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

conda init bash
exit

conda config --add default_channels https://repo.anaconda.com/pkgs/main
conda config --prepend channels https://public.dhe.ibm.com/ibmdl/export/pub/software/server/ibm-ai/conda/

#conda update -n base -c defaults conda

#https://stackoverflow.com/a/61387145/12865444
conda create -n ai python=3.7
conda activate ai
conda install --strict-channel-priority tensorflow-gpu

pip3 install gdown
conda install -c conda-forge matplotlib-base pandas scikit-learn

cd /mydata/
#https://www.nvidia.com/Download/driverResults.aspx/164093/en-us
wget https://us.download.nvidia.com/tesla/440.118.02/NVIDIA-Linux-ppc64le-440.118.02.run
sudo sh NVIDIA-Linux-ppc64le-440.118.02.run
sudo reboot now -h
sudo sh NVIDIA-Linux-ppc64le-440.118.02.run
nvidia-smi

#https://github.com/tensorflow/tensorflow/issues/4078#issuecomment-255129832
sudo find /usr/ -name 'libcuda.so.1'
#scp /usr/lib/powerpc64le-linux-gnu/libcuda.so.1 /mydata/miniconda3/envs/ai/cuda/lib/
scp /usr/lib/powerpc64le-linux-gnu/libcuda.so.1 /mydata/miniconda3/cuda/lib

# Disable yes to all
unset CONDA_ALWAYS_YES

python3
import tensorflow as tf
tf.config.list_physical_devices('GPU')