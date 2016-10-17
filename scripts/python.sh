#!/usr/bin/env bash

CAGE_NAME=`basename $CAGE_ENV`

cage.py app:addfiles ${CAGE_NAME} -f \.
cage.py app:run ${CAGE_NAME} -s "python $*"
