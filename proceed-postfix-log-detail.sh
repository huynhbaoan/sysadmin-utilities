#!/bin/bash
# set -e

### Input postfix log in /var/log/maillog-zzz
SRC_FILE="$1"


### Output report to file
DST_FILE=$HOME/$(echo $SRC_FILE | tr -s '/' | rev | cut -d '/' -f 1 | rev)-detail
[[ -f "$DST_FILE"  ]] && { echo "$DST_FILE is existing". Script will exit now.; exit 1; } || { echo "Creating $DST_FILE from $SRC_FILE"; touch $SRC_FILE; }


### Init variables
sent=0
bounced=0
defer=0



while IFS= read -r line
do
        grep -cq "client=" <<< "$line"
        if [[ $? -eq "0" ]]
        then
                echo "sent=$sent bounced=$bounced defer=$defer" >> $DST_FILE

                echo -n "$line " >> $DST_FILE

                sent=0
                bounced=0
                defer=0
        fi

        grep -cq "from=" <<< "$line"
        if [[ $? -eq "0" ]]
        then
                echo "$line" | awk '{print $7" "}' >> $DST_FILE
        fi

        grep -cq "status=sent" <<< "$line"
        if [[ $? -eq "0" ]]
        then
                echo "$line" | tr -s ' ' | cut -d " " -f 7,12 >> $DST_FILE
                let "sent=sent+1"
        fi

        grep -cq "status=bounced" <<< "$line"
        if [[ $? -eq "0" ]]
        then
		echo "$line" | tr -s ' ' | cut -d " " -f 7,12- >> $DST_FILE
                let "bounced=bounced+1"
        fi

        grep -cq "status=defer" <<< "$line"
        if [[ $? -eq "0" ]]
        then
		echo "$line" | tr -s ' ' | cut -d " " -f 7,12- >> $DST_FILE
                let "defer=defer+1"
        fi

        # echo "$line" | awk '{print $7, $12}'

done < $SRC_FILE
