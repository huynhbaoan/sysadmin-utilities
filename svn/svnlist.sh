#!/bin/bash
WORKING_DIR="/root/svnbackup_report/"
SCRIPT_DIR="/root/anhuynh/svn/"

cd /svn

### Get list of svn repo
ls /svn/ -I lost\+found -I svnbackup -I postfix -I phuongrepo -I ittest > $WORKING_DIR"svnrepolist"
# Remove empty dir
while read LINE;
do
    find $LINE -maxdepth 0 -empty -exec sed -i "/\b\({}\)\b/d" $WORKING_DIR"svnrepolist"  \;
done < $WORKING_DIR"svnrepolist"



### Generate list of latest file with last modified time
echo -n > $WORKING_DIR"svnrepotime"
while read p; 
do
    source $SCRIPT_DIR"newfile_scan.sh" $p | tee -a $WORKING_DIR"svnrepotime"
    echo $p | tee -a $WORKING_DIR"svnrepotime"
done < $WORKING_DIR"svnrepolist"



### Join list of name and timestampt
echo -n > $WORKING_DIR"svnrepotimepath"
while read line1 && read line2
do
    bothlines=$line1\ $line2
    echo $bothlines | tee -a $WORKING_DIR"svnrepotimepath"
done < $WORKING_DIR"svnrepotime"



### Determine year, month, day as timestamp limit: file with older timestampt is archived to Glacier
YEARP=$(date +%Y -d "150 day ago")
MONTHP=$(date +%m -d "150 day ago")
DAYP=$(date +%d -d "150 day ago")

echo -n > $WORKING_DIR"svndump.list"
while read LINE; 
do
### Extract year, month, day from lastest files
YEARF=$(echo $LINE | cut -d' ' -f1 -s | cut -d'-' -f1 -s)
MONTHF=$(echo $LINE | cut -d' ' -f1 -s | cut -d'-' -f2 -s)
DAYF=$(echo $LINE | cut -d' ' -f1 -s | cut -d'-' -f3 -s)
PATHF=$(echo $LINE | cut -d' ' -f5 -s)
### 
if [[ YEARF -lt YEARP  ]]
then
    echo "to Glacier, Year, $PATHF"
elif [[ YEARF -gt YEARP  ]]
then
    echo "new, to S3, $PATHF"
    echo $PATHF >> $WORKING_DIR"svndump.list"
else
    if [[ MONTHF -lt MONTHP  ]]
    then
        echo "to Glacier, Month, $PATHF"
    elif [[ MONTHF -gt MONTHP  ]]
    then
        echo "new, to S3, $PATHF"
        echo $PATHF >> $WORKING_DIR"svndump.list"
    else
        if [[ DAYF -lt DAYP  ]]
        then
            echo "to Glacier, Day, $PATHF"
        else
            echo "new, to S3, $PATHF"
            echo $PATHF >> $WORKING_DIR"svndump.list"
        fi
    fi
fi
done < $WORKING_DIR"svnrepotimepath"



### Now, dump recently changed svn repos
source $SCRIPT_DIR"svndump.sh"
