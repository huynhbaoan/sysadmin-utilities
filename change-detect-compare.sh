#!/bin/bash
# set -uxo pipefail
# set -Ee

export LC_ALL=C

start=`date +%s`

md5sum -c --quiet /tmp/checksum 2>&1 > /tmp/check-result

find -L /etc/ -type f -not -path "/etc/httpd/logs/*" -print0 | sort -z | tr '\0' '\n' > /tmp/checklist-after
find -L /usr/bin -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist-after
find -L /usr/etc -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist-after
find -L /usr/include -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist-after
find -L /usr/lib -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist-after
find -L /usr/lib64 -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist-after
find -L /usr/libexec -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist-after
find -L /usr/sbin -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist-after

diff /tmp/checklist /tmp/checklist-after 2>&1 >> /tmp/check-result

end=`date +%s`
runtime=$((end-start))
echo "Execution time: $runtime"
