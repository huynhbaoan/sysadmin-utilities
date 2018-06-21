#!/bin/bash
set -x
while read LINE
do
    /usr/bin/svnadmin dump --deltas /svn/"$LINE"/ | gzip -5 > /svnbackup/"$LINE".dump.gz 2> /root/anhuynh/svndump.err
done < /root/anhuynh/svndump.list
