#!/bin/bash
WORKING_DIR="/root/svnbackup_report/"
IDENTITY="/root/.anhuynh/.ssh/id_rsa"

### INIT log date
echo $(date '+%d-%m-%Y_%H-%M-%S') >> $WORKING_DIR"syncfile.err"
echo $(date '+%d-%m-%Y_%H-%M-%S') >> $WORKING_DIR"syncfile.log"

### Give proper permission to dest. dir
ssh -i $IDENTITY gsysadmin@192.168.38.130 'sudo chown -R gsysadmin: /git/svnbackup/ && sudo chmod 750 /git/svnbackup/ && sudo rm -f /git/svnbackup/*.dump.gz'
rsync -avzp -e "ssh -i $IDENTITY" --remove-source-files /svnbackup/*.dump.gz gsysadmin@192.168.38.130:/git/svnbackup/
