#!/usr/bin/env bash

CAGE_NAME=`basename $CAGE_ENV`

cage app:addfiles ${CAGE_NAME} -f \.

if ! [ -z "${PORT+_}" ] ; then
    cage app:run ${CAGE_NAME} -s "python $*" -P ${PORT}
else
    cage app:run ${CAGE_NAME} -s "python $*"
fi
