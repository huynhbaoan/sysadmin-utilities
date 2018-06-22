#!/bin/bash
### Run by gsysadmin, on 192.168.38.130
while read LINE
do
    /home/gsysadmin/.local/bin/aws glacier upload-archive --account-id - --vault-name gnt-it-archive --body /git/svnbackup/"$LINE" | tee -a /git/svnbackup/"$LINE".json
done < /git/svnbackup/upload.list

