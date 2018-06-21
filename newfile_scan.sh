#!/bin/bash
FINDPATH=$1
if [[ -e "$FINDPATH"/db/txn-current ]]
then
    stat --format '%Y :%y %n' "$FINDPATH"/db/txn-current | cut -d: -f2-
else
    if [[ -d "$FINDPATH"/db  ]]
    then
        find "$FINDPATH"/db -type f -print0 | xargs -0 stat --format '%Y :%y %n' | sort -nr | cut -d: -f2- | head -n 1
    else
        find "$FINDPATH" -type f -print0 | xargs -0 stat --format '%Y :%y %n' | sort -nr | cut -d: -f2- | head -n 1
    fi
fi
