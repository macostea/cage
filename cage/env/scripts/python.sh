#!/usr/bin/env bash

# Run the command
CAGE_NAME=`basename $CAGE_ENV`

cage app:addfiles ${CAGE_NAME} -f \.

if ! [ -z "${ENV+_}" ] ; then
    cage app:run ${CAGE_NAME} -s "python $*" -e ${ENV}
else
    if [ -f ENV ] ; then
        cage app:run ${CAGE_NAME} -s "python $*" -e ENV
    else
        cage app:run ${CAGE_NAME} -s "python $*"
    fi
fi
