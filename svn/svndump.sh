#!/bin/bash
set -x
WORKING_DIR="/root/svnbackup_report"
echo $(date '+%d-%m-%Y_%H-%M-%S') >> $WORKING_DIR"svndump.err"
while read LINE
do
    /usr/bin/svnadmin dump --deltas /svn/$LINE/ | gzip -5 > /svnbackup/$LINE"_"$(date '+%d-%m-%Y_%H-%M-%S').dump.gz 2>> $WORKING_DIR"svndump.err"
done < $WORKING_DIR"svndump.list"
