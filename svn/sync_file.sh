#!/bin/bash
WORKING_DIR="/root/svnbackup_report/"
IDENTITY="/root/.anhuynh/.ssh/id_rsa"

### INIT log date
echo $(date '+%d-%m-%Y_%H-%M-%S') >> $WORKING_DIR"syncfile.log"

### Give proper permission to dest. dir
ssh -i $IDENTITY gsysadmin@192.168.38.130 "sudo chown -R gsysadmin: /git/svnbackup/ && sudo chmod 750 /git/svnbackup/ && sudo rm -f /git/svnbackup/*.dump.gz"
ssh -i $IDENTITY gsysadmin@192.168.38.130 "sudo chown -R gsysadmin: /git/svnbackup/ && sudo chmod 750 /git/svnbackup/"



### Due to lacking of disk space on Git server, we rsync 1 file to Git server, upload file from Git server to S3, delete uploaded file, then repeat

### Get list of upload file
ls /svnbackup/ | grep "dump.gz" > $WORKING_DIR"s3_upload.list"

### Sync each file and check if file uploading is completed
while read LINE
do
    rsync -avzp -e "ssh -i $IDENTITY" --remove-source-files /svnbackup/$LINE gsysadmin@192.168.38.130:/git/svnbackup 2>&1 | tee -a $WORKING_DIR"syncfile.log"
    ssh -n -i $IDENTITY gsysadmin@192.168.38.130 "/git/svnbackup/s3_upload.sh"
    rsync -avzp -e "ssh -i $IDENTITY" gsysadmin@192.168.38.130:/git/svnbackup/s3_uploaded.list $WORKING_DIR 2>&1 | tee -a $WORKING_DIR"syncfile.log"
    while ! grep -Fxq $LINE $WORKING_DIR"s3_uploaded.list"
    do
        sleep 10m
        rsync -avzp -e "ssh -i $IDENTITY" gsysadmin@192.168.38.130:/git/svnbackup/s3_uploaded.list $WORKING_DIR 2>&1 | tee -a $WORKING_DIR"syncfile.log"
    done
done < $WORKING_DIR"s3_upload.list"


### Cleanup 
mv $WORKING_DIR"s3_uploaded.list" $WORKING_DIR"s3_uploaded.list_"$(date '+%d-%m-%Y_%H-%M-%S')
ssh -i $IDENTITY gsysadmin@192.168.38.130 "sudo rm /git/svnbackup/s3_uploaded.list"
