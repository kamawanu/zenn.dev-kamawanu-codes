#!/bin/bash -x
set -xe
MYPRJ=$( cut -d. -f1 < APPVER )
export CLOUDSDK_CORE_PROJECT=$MYPRJ
VERSION=$( cut -d. -f2 < APPVER )
###. $HOME/google-cloud-sdk/path.bash.inc # これ重要
####gcloud app deploy --no-promote --
DIR=.
if [ -f app/app.yaml ]
then
    DIR=app
    hg addr $DIR
    find $DIR -name "*.pyc" -exec rm -rfv "{}" ";"
fi
###ls -C
OV=$( curl -qs https://$VERSION-dot-$MYPRJ.appspot.com/isversion )
bash -xe ./gcloudrun.sh gcloud app deploy $DIR --no-promote --version=$VERSION  
NV=$( curl -qs https://$VERSION-dot-$MYPRJ.appspot.com/isversion )
hg qnew $NV
hg qfinish -a
