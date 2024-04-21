#!/bin/bash -x
if [ \! -f .venv/bin/activate ]
then
    python3 -mvenv .venv
fi
. ./.venv/bin/activate
pip3 install django
##django-admin createproject formtest
