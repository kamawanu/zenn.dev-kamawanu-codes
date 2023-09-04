#!/bin/bash -x
#####. $HOME/google-cloud-sdk/path.bash.inc # これ重要
MYPRJ=$( cut -d. -f1 < APPVER )
MYIP=0.0.0.0
DEVAPP=$( . ./gcloudrun.sh which dev_appserver.py )
##PYTHON2=$( which python | which python3 )
#PATH=.:$PATH
# https://github.com/firebase/firebase-tools/issues/4336
export JAVA_TOOL_OPTIONS="-Xmx4g"
. ./gcloudrun.sh python3 $DEVAPP \
-A $MYPRJ \
--port 8110 --host $MYIP \
--admin_port 8112 --admin_host $MYIP \
--enable_host_checking 0 \
--support_datastore_emulator=yes \
--datastore_emulator_port=8200 \
--skip_sdk_update_check --storage_path dbemulate/ app/
