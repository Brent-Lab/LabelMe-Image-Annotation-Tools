#!/bin/bash

if [ $# -eq 0 ]
then
    echo "Missing arguments"
    exit 1
fi

FOLDER="$1"

if [[ ! $FOLDER == */ ]]
then
    FOLDER="${FOLDER}/"
fi

if [ ! -d "$PWD/$FOLDER" ]; then
    echo "Folder does not exist"
    exit 1
fi

read -p 'What object would you like to remove?' OBJECTNAME
python removeObject.py "${FOLDER}" ${OBJECTNAME}
echo "Done"