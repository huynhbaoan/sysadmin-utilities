#!/bin/bash
WORKING_DIR="/root/svnbackup_report/"
SCRIPT_DIR="/root/anhuynh/svn/"

### Scan svn directory and generate list of recently changed repos to dump
source $SCRIPT_DIR"svnlist.sh"
### Now, dump recently changed svn repos
source $SCRIPT_DIR"svndump.sh"
### Rsync dumped file to Git server, upload, then delete dumped source file
source $SCRIPT_DIR"sync_file.sh"
