#!/bin/bash
export LC_ALL=C

inspector_cve_list="$1"
output_report="/root/redhat-cve-report.txt"

echo -n > $output_report

while IFS= read -r line
do
        ### Extract record from Redhat CVE DB
        payload=$(curl "https://access.redhat.com/hydra/rest/securitydata/cve/$line.json")
        threat_severity=$(echo $payload | jq -r '.threat_severity')
        public_date=$(echo $payload | jq -r '.public_date')
        cvss3_scoring_vector=""
        cvss3_scoring_vector_test=$(echo $payload | jq -r '.cvss3.cvss3_scoring_vector')
        if [[ $cvss3_scoring_vector_test != "null" ]]; then cvss3_scoring_vector=$(echo $payload | jq -r '.cvss3.cvss3_scoring_vector'); cvss3_base_score=$(echo $payload | jq -r '.cvss3.cvss3_base_score'); status=$(echo $payload | jq -r '.cvss3.status'); fi
        cvss3_scoring_vector_test=$(echo $payload | jq -r '.cvss2.cvss2_scoring_vector')
        if [[ $cvss3_scoring_vector_test != "null" ]]; then cvss3_scoring_vector=$(echo $payload | jq -r '.cvss2.cvss2_scoring_vector'); cvss3_base_score=$(echo $payload | jq -r '.cvss2.cvss2_base_score'); status=$(echo $payload | jq -r '.cvss2.status'); fi
        cvss3_scoring_vector_test=$(echo $payload | jq -r '.cvss.cvss_scoring_vector')
        if [[ $cvss3_scoring_vector_test != "null" ]]; then cvss3_scoring_vector=$(echo $payload | jq -r '.cvss.cvss_scoring_vector'); cvss3_base_score=$(echo $payload | jq -r '.cvss.cvss_base_score'); status=$(echo $payload | jq -r '.cvss.status'); fi
        echo $cvss3_scoring_vector
        cvss3_attack_vector=$(echo $cvss3_scoring_vector | cut -d / -f 2)
        cvss3_attack_complexity=$(echo $cvss3_scoring_vector | cut -d / -f 3)
        cvss3_attack_privileges_required=$(echo $cvss3_scoring_vector | cut -d / -f 4)
        cvss3_attack_user_interaction=$(echo $cvss3_scoring_vector | cut -d / -f 5)
        cvss3_attack_scope=$(echo $cvss3_scoring_vector | cut -d / -f 6)
        cvss3_attack_confidentiality_impact=$(echo $cvss3_scoring_vector | cut -d / -f 7)
        cvss3_attack_integrity_impact=$(echo $cvss3_scoring_vector | cut -d / -f 8)
        cvss3_attack_availability_impact=$(echo $cvss3_scoring_vector | cut -d / -f 9)
        details=$(echo $payload | jq -r '.details | .[]' | tr '\n' ' ')

        ### Merge result to 1 line
        echo -e "$line\t$threat_severity\t$public_date\t$cvss3_base_score\t$cvss3_attack_vector\t$cvss3_attack_complexity\t$cvss3_attack_privileges_required\t$cvss3_attack_user_interaction\t$cvss3_attack_scope\t$cvss3_attack_confidentiality_impact\t$cvss3_attack_integrity_impact\t$cvss3_attack_availability_impact\t$status\t$details" >> $output_report

done < $inspector_cve_list