#!/bin/bash

FILES=*
for file in $FILES ; do
    if [ "${file: -3}" == ".sh" ]
    then
        echo "Processing $file file..."
        tr -d '\r' < $file > $file.tmp
        rm -f $file
        mv $file.tmp $file
        chmod +x $file
    fi
done
