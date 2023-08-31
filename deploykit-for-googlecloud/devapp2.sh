#!/bin/bash -x
#####. $HOME/google-cloud-sdk/path.bash.inc # これ重要
MYPRJ=$( cut -d. -f1 < APPVER )
MYIP=0.0.0.0
DEVAPP=$( . ./gcloudrun.sh which dev_appserver.py )
##PYTHON2=$( which python | which python3 )
#PATH=.:$PATH
. ./gcloudrun.sh python3 $DEVAPP \
-A $MYPRJ \
--port 8110 --host $MYIP \
--admin_port 8112 --admin_host $MYIP \
--enable_host_checking 0 \
--skip_sdk_update_check --storage_path webdb/ app/
