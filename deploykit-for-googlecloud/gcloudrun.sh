#!/bin/bash -x
set -e
#V=370.0.0
if [ -f env ]
then
	. ./env
fi

if [ \! -d $HOME/google-cloud-sdk ]
then
    OS=$( uname -s -m | sed -e "s/ /-/g" | tr [:upper:] [:lower:] )
    V=440.0.0
    case $OS in
    linux-*)
        # https://cloud.google.com/sdk/docs/install#linux
        #V=370.0.0
        ;;
    darwin-x86_64)
        # https://cloud.google.com/sdk/docs/install#mac
        #V=365.0.0
        OS=darwin-x86
        ;;
    esac

    wget -N https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-$V-$OS.tar.gz
    # https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-370.0.0-darwin-x86_64.tar.gz
    tar xvfkz google-cloud-sdk-$V-$OS.tar.gz -C $HOME

    fgrep google-cloud-sdk/path.bash.inc $HOME/.bashrc || (
        cd $HOME/google-cloud-sdk
        ./install.sh --path-update true --rc-path $HOME/.bashrc
    )

    #fgrep google-cloud-sdk/path.bash.inc $HOME/.bashrc
    which gcloud || . $HOME/google-cloud-sdk/path.bash.inc
    gcloud components reinstall
    gcloud components install app-engine-python 
fi
#set -xe
MYPRJ=$( cut -d. -f1 < APPVER )
export CLOUDSDK_CORE_PROJECT=$MYPRJ
VERSION=$( cut -d. -f2 < APPVER )

. $HOME/google-cloud-sdk/path.bash.inc
exec nice $*
