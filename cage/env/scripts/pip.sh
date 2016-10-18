#!/usr/bin/env bash

CAGE_NAME=`basename $CAGE_ENV`

# Usually called with pip install <something> or pip install -r <something>
# Only support the requirements file for now

if [ "-r" == "$2" ]; then
    cage app:addfiles ${CAGE_NAME} -f \.
    cage app:deps ${CAGE_NAME} -r $3
fi
