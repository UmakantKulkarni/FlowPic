#!/usr/bin/bash

apt-get update && apt-get -y upgrade && apt-get update

apt -y install curl wget apache2-utils default-jre default-jdk wget git vim nano make g++ net-tools iproute2 libssl-dev tcpdump jq iputils-ping apt-transport-https nghttp2-client bash-completion xauth gcc autoconf libtool pkg-config sshpass python3 python3-setuptools python3-pip qt5-default x11-apps feh python3-virtualenv

cd /mydata/
mkdir tmp
cd /mydata && git clone https://github.com/UmakantKulkarni/scripts
 
# For ppc64el, cuDNN is 8.0.5 & CUDA is 10.2. Accordingly, chose run file from this website - https://www.nvidia.com/Download/index.aspx?lang=en-us and cuDNN file from this website - https://developer.nvidia.com/rdp/cudnn-archive 

#https://www.nvidia.com/Download/driverResults.aspx/164093/en-us
wget https://us.download.nvidia.com/tesla/440.118.02/NVIDIA-Linux-ppc64le-440.118.02.run
sudo sh NVIDIA-Linux-ppc64le-440.118.02.run
sudo reboot now -h
sudo sh NVIDIA-Linux-ppc64le-440.118.02.run
nvidia-smi

# https://developer.nvidia.com/compute/machine-learning/cudnn/secure/8.0.5/10.2_20201106/cudnn-10.2-linux-ppc64le-v8.0.5.39.tgz
# Download on Mac and copy it to server
tar xvf cudnn-10.2-linux-ppc64le-v8.0.5.39.tgz
sudo find /usr/ -name '*cuda*.h'
sudo cp -P cuda/targets/ppc64le-linux/include/* /usr/include/linux/
mkdir /usr/lib/cuda
sudo cp -P cuda/targets/ppc64le-linux/lib/* /usr/lib/cuda/
sudo find /usr/ -name 'libcuda.so.1'
cp /usr/lib/powerpc64le-linux-gnu/libcuda.so.1 /usr/lib/cuda/

#export 'PATH=/mydata/cuda/bin/:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH="/usr/lib/cuda/:$LD_LIBRARY_PATH"' >> ~/.bashrc
source ~/.bashrc

cd /mydata
wget https://oplab9.parqtec.unicamp.br/pub/ppc64el/bazel/ubuntu_18.04/bazel_bin_ppc64le_4.2.2
./bazel_bin_ppc64le_4.2.2
cp bazel_bin_ppc64le_4.2.2 /usr/bin/bazel

cd /mydata/flow_pic
virtualenv flow_pic_ml
source flow_pic_ml/bin/activate

cd /mydata/
mkdir flow_pic
cd flow_pic
#https://www.tensorflow.org/install/source
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
git checkout r2.7
./configure
/mydata/flow_pic/flow_pic_ml/bin/python3
#n y n 11 8 /usr/include/linux/, /usr/lib/cuda 

export HOME=/mydata/temp/
bazel --output_base=/mydata/tmp/
bazel --output_user_root=/mydata/tmp/
bazel clean
bazel build -c opt --config=cuda //tensorflow/tools/pip_package:build_pip_package 
./bazel-bin/tensorflow/tools/pip_package/build_pip_package /mydata/

cd /mydata/flow_pic
source flow_pic_ml/bin/activate
pip3 install /mydata/tensorflow-2.8.0-cp38-cp38-linux_x86_64.whl

python3
import tensorflow as tf
tf.config.list_physical_devices('GPU')


cd /mydata/
mkdir flow_pic
cd flow_pic
git clone https://github.com/UmakantKulkarni/FlowPic
cd FlowPic/
git checkout uk1
git pull
cd ..
gdown --id 1gz61vnMANj-4hKNvZv1KFK9LajR91X-m
unzip FlowPic_raw_csvs.zip
mv classes_csvs classes
cd FlowPic/
./traffic_csv_converter.py 
./npzToNpyDs.py
./overlap_multiclass_reg_non_bn.py


echo "Finished running setup-node.sh"


#One or more modprobe configuration files to disable Nouveau have been written.  For some distributions, this may be sufficient to disable Nouveau; other distributions may require modification of the initial ramdisk.  Please reboot your system and attempt NVIDIA driver installation again.  Note if you later wish to reenable Nouveau, you will need to delete these files: /usr/lib/modprobe.d/nvidia-installer-disable-nouveau.conf, /etc/modprobe.d/nvidia-installer-disable-nouveau.conf   