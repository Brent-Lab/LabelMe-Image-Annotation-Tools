#!/bin/bash

if [ $# -eq 0 ]
then
    echo "Missing arguments"
    exit 1
fi

FOLDER=$1

if [[ ! $FOLDER == */ ]]
then
    FOLDER="${FOLDER}/"
fi

if [ ! -d "$PWD/$FOLDER" ]; then
    echo "Folder does not exist"
    exit 1
fi

echo "Do you wish to rename files?"
select yn in "Yes" "No"; do
    case $yn in
        Yes )
            read -p 'Enter name for objects in folder: ' OBJECTNAMES
            python rename_files.py ${FOLDER} ${OBJECTNAMES}
            FOLDER=$(ls -td */ | head -1)
            echo "New folder saved as ${FOLDER}"
            echo "Target directory changed to ${FOLDER}"
            break;;
        No ) break;;
    esac
done

echo "\nDo you wish to convert to COCO format?"
select yn in "Yes" "No"; do
    case $yn in
        Yes )
            if [[ -f "${PWD}/${FOLDER}trainval.json" ]]; then
                rm "${PWD}/${FOLDER}trainval.json"
                echo "Removed previous coco file in directory"
            fi
            python labelme2coco.py "${FOLDER}" --output="${FOLDER}trainval.json"
            break;;
        No ) break;;
    esac
done

echo "\nDo you wish to append EXIF data to images?"
select yn in "Yes" "No"; do
    case $yn in
        Yes )
            python append_exif.py "${FOLDER}"
            break;;
        No ) break;;
    esac
done

echo "Done"
