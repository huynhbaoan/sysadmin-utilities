#!/bin/bash
# set -e

### Input postfix log in /var/log/maillog-zzz
FILE="$1"


### Check if this script is run as root.
### nice command need root privilege to set process priority
[[ $EUID -ne 0 ]] && { echo "Please re-run this script with root privilege."; return 1; }


### Init variables
SRC_FILE=""
DST_FILE=""


### Check log file if log file is compressed. If yes, extract.
gzip -t $FILE
if [[ $? -eq 0 ]]; then
	FILEEXTRACT=$HOME/$(echo $FILE | tr -s '/' | rev | cut -d '/' -f 1 | cut -d '.' -f 2 | rev)
	echo "Decompressing $FILE to $FILEEXTRACT"
	nice -n 19 zcat $FILE > $FILEEXTRACT

	# Handle extracted log file as normal file
	DST_FILE=$FILEEXTRACT-sent
	SRC_FILE=$FILEEXTRACT
else
	# Handle normal file
	DST_FILE=$HOME/$(echo $FILE | tr -s '/' | rev | cut -d '/' -f 1 | rev)-sent
	SRC_FILE=$FILE
fi


### Check if we have existing extracted log. If yes, exit.
[[ -f "$DST_FILE"  ]] && { echo "$DST_FILE is existing". Script will exit now.; return 1; } || { echo "Creating $DST_FILE from $SRC_FILE"; touch $SRC_FILE; }

### Grep and sort log entries
echo "Extracting logs record from $SRC_FILE to $DST_FILE ..."
grep "client=" $SRC_FILE | awk {'print $6'} | xargs -I % bash -c "nice -n 19 grep % $SRC_FILE" > "$DST_FILE"
