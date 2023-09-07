#!/bin/bash -x
#####. $HOME/google-cloud-sdk/path.bash.inc # これ重要
MYPRJ=$( cut -d. -f1 < APPVER )
MYIP=0.0.0.0
DEVAPP=$( . ./gcloudrun.sh which dev_appserver.py )
##PYTHON2=$( which python | which python3 )
#PATH=.:$PATH
# https://github.com/firebase/firebase-tools/issues/4336
export JAVA_TOOL_OPTIONS="-Xmx4g"
# https://stackoverflow.com/questions/73661666/dev-appserver-py-badargumenterror-app-must-not-be-empty
#export APPLICATION_ID=dev~None
#Noneにしないとdevappserverの管理画面が正常に動かないが、
#Noneだと今度はdatastoreからのimport/exportに失敗する（データは入ってるっぽいが参照できない）
#どうしろと...
. ./gcloudrun.sh python3 $DEVAPP \
-A $MYPRJ \
--port 8110 --host $MYIP \
--enable_host_checking 0 \
--skip_sdk_update_check $* app/
