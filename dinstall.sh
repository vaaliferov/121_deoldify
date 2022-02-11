#!/usr/bin/env bash

MODEL_FILE_NAME=ColorizeStable_gen.pth
DEOLDIFY_REPO_URL='https://github.com/jantic/DeOldify.git'
MODEL_URL='https://www.dropbox.com/s/usf7uifrctqw9rl/ColorizeStable_gen.pth?dl=0'

apt update
apt install -y wget
apt install -y python3-pip
apt install -y python3-opencv

pip3 install cython wheel
pip3 install -r requirements.txt

mkdir models
wget $MODEL_URL -O models/$MODEL_FILE_NAME
git clone $DEOLDIFY_REPO_URL ./
mv DeOldify/deoldify ./
rm -rf DeOldify