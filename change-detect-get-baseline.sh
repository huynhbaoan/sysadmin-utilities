#!/bin/bash
# set -uxo pipefail
# set -Ee

export LC_ALL=C

start=`date +%s`

find -L /etc/ -type f -not -path "/etc/httpd/logs/*" -print0 | sort -z | xargs -0 -r md5sum > /tmp/checksum
find -L /usr/bin -type f -print0 | sort -z | xargs -0 -r md5sum >> /tmp/checksum
find -L /usr/etc -type f -print0 | sort -z | xargs -0 -r md5sum >> /tmp/checksum
find -L /usr/include -type f -print0 | sort -z | xargs -0 -r md5sum >> /tmp/checksum
find -L /usr/lib -type f -print0 | sort -z | xargs -0 -r md5sum >> /tmp/checksum
find -L /usr/lib64 -type f -print0 | sort -z | xargs -0 -r md5sum >> /tmp/checksum
find -L /usr/libexec -type f -print0 | sort -z | xargs -0 -r md5sum >> /tmp/checksum
find -L /usr/sbin -type f -print0 | sort -z | xargs -0 -r md5sum >> /tmp/checksum

find -L /etc/ -type f -not -path "/etc/httpd/logs/*" -print0 | sort -z | tr '\0' '\n' > /tmp/checklist
find -L /usr/bin -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist
find -L /usr/etc -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist
find -L /usr/include -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist
find -L /usr/lib -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist
find -L /usr/lib64 -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist
find -L /usr/libexec -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist
find -L /usr/sbin -type f -print0 | sort -z | tr '\0' '\n' >> /tmp/checklist

end=`date +%s`
runtime=$((end-start))
echo "Execution time: $runtime"
