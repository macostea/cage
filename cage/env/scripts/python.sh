#!/usr/bin/env bash

CAGE_NAME=`basename $CAGE_ENV`

cage app:addfiles ${CAGE_NAME} -f \.
cage app:run ${CAGE_NAME} -s "python $*"
