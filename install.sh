#!/usr/bin/env bash

USER='ubuntu'
NAME='deoldify'

DIR=/opt/$NAME
SERVICE_NAME="${NAME}_bot.service"
SERVICE_FILE_PATH=/etc/systemd/system/$SERVICE_NAME

MODEL_FILE_NAME=ColorizeStable_gen.pth
DEOLDIFY_REPO_URL='https://github.com/jantic/DeOldify.git'
MODEL_URL='https://www.dropbox.com/s/usf7uifrctqw9rl/ColorizeStable_gen.pth?dl=0'

rm -rf $DIR $SERVICE_FILE_PATH
systemctl disable --now $SERVICE_NAME

cat bot.service > $SERVICE_FILE_PATH
sed -i "s/<name>/$NAME/g" $SERVICE_FILE_PATH
sed -i "s/<user>/$USER/g" $SERVICE_FILE_PATH

mkdir $DIR $DIR/env $DIR/models
apt install -y wget git python3-opencv
apt install -y python3-pip python3-venv
pip3 install -U virtualenv
python3 -m venv $DIR/env

source $DIR/env/bin/activate
pip3 install --no-cache-dir cython wheel
pip3 install --no-cache-dir -r requirements.txt
deactivate

cp -r . $DIR
wget $MODEL_URL -O $DIR/models/$MODEL_FILE_NAME
git clone $DEOLDIFY_REPO_URL $DIR/repo
mv $DIR/repo/deoldify $DIR/
rm -rf $DIR/repo

chmod 755 $DIR
chown -R $USER:$USER $DIR

systemctl daemon-reload
systemctl enable --now $SERVICE_NAME