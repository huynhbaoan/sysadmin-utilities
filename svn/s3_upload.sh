#!/bin/bash
### Run by gsysadmin, on 192.168.38.130
cd /git/svnbackup/

### Get list file to upload
ls /git/svnbackup/|grep -i "dump.gz" > /git/svnbackup/s3_upload.list
### Upload, write log, then delete uploaded file
### Note: fail upload also caught file to be deleted
while read LINE
do
    sudo -i -u gsysadmin /home/gsysadmin/.local/bin/aws s3 cp /git/svnbackup/$LINE s3://gnt-it-backup/svn/ --storage-class ONEZONE_IA && (echo $LINE >> /git/svnbackup/s3_uploaded.list) || (echo $LINE" failed" >> /git/svnbackup/s3_uploaded.list)
    sudo rm -f /git/svnbackup/$LINE
done < /git/svnbackup/s3_upload.list

