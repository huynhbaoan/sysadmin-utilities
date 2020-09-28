#!/bin/bash
export LC_ALL=C

inspector_cve_list="$1"
output_report="/root/redhat-cve-report.txt"

echo -n > $output_report
echo -e "CVE ID\tThreat Severity\tPublic Date\tCVSS Version\tCVSS Score\tAttack Vector\tAttack Complexity\tPrivileges Required\tUser Interaction required\tScope\tConfidentiality Impact\tIntegrity Impact\tAvailability Impact\tStatus\tDetails" >> $output_report
cvss3_base_score=""
cvss3_scoring_vector=""
cvss3_scoring_vector_test=""

while IFS= read -r line
do
	### Extract record from Redhat CVE DB
	payload=$(curl "https://access.redhat.com/hydra/rest/securitydata/cve/$line.json")
	threat_severity=$(echo $payload | jq -r '.threat_severity')
	public_date=$(echo $payload | jq -r '.public_date')
	
	### Examine cvss data, from version 3 to 1
	cvss3_scoring_vector_test=$(echo $payload | jq -r '.cvss3.cvss3_scoring_vector')
	if [[ $cvss3_scoring_vector_test != "null" ]]
	then
		cvss3_scoring_vector=$(echo $payload | jq -r '.cvss3.cvss3_scoring_vector'); cvss3_base_score=$(echo $payload | jq -r '.cvss3.cvss3_base_score'); status=$(echo $payload | jq -r '.cvss3.status')
		cvss3_version=$(echo $cvss3_scoring_vector | cut -d / -f 1)
		cvss3_attack_vector=$(echo $cvss3_scoring_vector | cut -d / -f 2)
		cvss3_attack_complexity=$(echo $cvss3_scoring_vector | cut -d / -f 3)
	        cvss3_attack_privileges_required=$(echo $cvss3_scoring_vector | cut -d / -f 4)
        	cvss3_attack_user_interaction=$(echo $cvss3_scoring_vector | cut -d / -f 5)
	        cvss3_attack_scope=$(echo $cvss3_scoring_vector | cut -d / -f 6)
        	cvss3_attack_confidentiality_impact=$(echo $cvss3_scoring_vector | cut -d / -f 7)
	        cvss3_attack_integrity_impact=$(echo $cvss3_scoring_vector | cut -d / -f 8)
        	cvss3_attack_availability_impact=$(echo $cvss3_scoring_vector | cut -d / -f 9)
	else
		cvss3_scoring_vector_test=$(echo $payload | jq -r '.cvss2.cvss2_scoring_vector')
        	if [[ $cvss3_scoring_vector_test != "null" ]]
		then 
			cvss3_scoring_vector=$(echo $payload | jq -r '.cvss2.cvss2_scoring_vector'); cvss3_base_score=$(echo $payload |jq -r '.cvss2.cvss2_base_score'); status=$(echo $payload | jq -r '.cvss2.status')
			cvss3_version="2"
                        cvss3_attack_vector=$(echo $cvss3_scoring_vector | cut -d / -f 1)
                        cvss3_attack_complexity=$(echo $cvss3_scoring_vector | cut -d / -f 2)
                        cvss3_attack_privileges_required=$(echo $cvss3_scoring_vector | cut -d / -f 3)
                        cvss3_attack_user_interaction="N/A"
                        cvss3_attack_scope="N/A"
                        cvss3_attack_confidentiality_impact=$(echo $cvss3_scoring_vector | cut -d / -f 4)
                        cvss3_attack_integrity_impact=$(echo $cvss3_scoring_vector | cut -d / -f 5)
                        cvss3_attack_availability_impact=$(echo $cvss3_scoring_vector | cut -d / -f 6)
		else
			cvss3_scoring_vector_test=$(echo $payload | jq -r '.cvss.cvss_scoring_vector')
			if [[ $cvss3_scoring_vector_test != "null" ]]
			then 
				cvss3_scoring_vector=$(echo $payload | jq -r '.cvss.cvss_scoring_vector'); cvss3_base_score=$(echo $payload | jq -r '.cvss.cvss_base_score'); status=$(echo $payload | jq -r '.cvss.status')
				cvss3_version="1"
		                cvss3_attack_vector=$(echo $cvss3_scoring_vector | cut -d / -f 1)
	        	        cvss3_attack_complexity=$(echo $cvss3_scoring_vector | cut -d / -f 2)
                		cvss3_attack_privileges_required=$(echo $cvss3_scoring_vector | cut -d / -f 3)
	        	        cvss3_attack_user_interaction="N/A"
        		        cvss3_attack_scope="N/A"
	                	cvss3_attack_confidentiality_impact=$(echo $cvss3_scoring_vector | cut -d / -f 4)
	                	cvss3_attack_integrity_impact=$(echo $cvss3_scoring_vector | cut -d / -f 5)
        		        cvss3_attack_availability_impact=$(echo $cvss3_scoring_vector | cut -d / -f 6)
			else
				cvss3_scoring_vector="null"; cvss3_base_score="null"; status="null"; cvss3_version="null"
                                cvss3_attack_vector=$(echo $cvss3_scoring_vector | cut -d / -f 1)
                                cvss3_attack_complexity=$(echo $cvss3_scoring_vector | cut -d / -f 2)
				cvss3_attack_privileges_required=$(echo $cvss3_scoring_vector | cut -d / -f 3)
                                cvss3_attack_user_interaction="N/A"
                                cvss3_attack_scope="N/A"
                                cvss3_attack_confidentiality_impact=$(echo $cvss3_scoring_vector | cut -d / -f 4)
                                cvss3_attack_integrity_impact=$(echo $cvss3_scoring_vector | cut -d / -f 5)
                                cvss3_attack_availability_impact=$(echo $cvss3_scoring_vector | cut -d / -f 6)
			fi
		fi

	fi
	echo $cvss3_scoring_vector
	details=$(echo $payload | jq -r '.details | .[]' | tr '\n' ' ')

	### Merge result to 1 line
	echo -e "$line\t$threat_severity\t$public_date\t$cvss3_version\t$cvss3_base_score\t$cvss3_attack_vector\t$cvss3_attack_complexity\t$cvss3_attack_privileges_required\t$cvss3_attack_user_interaction\t$cvss3_attack_scope\t$cvss3_attack_confidentiality_impact\t$cvss3_attack_integrity_impact\t$cvss3_attack_availability_impact\t$status\t$details" >> $output_report

done < $inspector_cve_list



### Decode CVSS value to human-readable value
sed -i 's/AV:A/Adjacent Network/g' $output_report
sed -i 's/AV:N/Network/g' $output_report
sed -i 's/AV:L/Local/g' $output_report
sed -i 's/AV:P/Physical/g' $output_report

sed -i 's/Au:N/None Authentication/g' $output_report
sed -i 's/Au:S/Single Authentication/g' $output_report
sed -i 's/PR:H/High Privileges/g' $output_report
sed -i 's/PR:L/Low Privileges/g' $output_report
sed -i 's/PR:N/None Privileges/g' $output_report

sed -i 's/AC:L/Low/g' $output_report
sed -i 's/AC:M/Medium/g' $output_report
sed -i 's/AC:H/High/g' $output_report

sed -i 's/UI:N/None/g' $output_report
sed -i 's/UI:R/Required/g' $output_report

sed -i 's/S:U/Unchanged/g' $output_report
sed -i 's/S:C/Changed/g' $output_report

sed -i 's/C:N/None/g' $output_report
sed -i 's/C:L/Low/g' $output_report
sed -i 's/C:P/Partial/g' $output_report
sed -i 's/C:H/High/g' $output_report

sed -i 's/I:N/None/g' $output_report
sed -i 's/I:L/Low/g' $output_report
sed -i 's/I:P/Partial/g' $output_report
sed -i 's/I:H/High/g' $output_report

sed -i 's/A:N/None/g' $output_report
sed -i 's/A:L/Low/g' $output_report
sed -i 's/A:P/Partial/g' $output_report
sed -i 's/A:H/High/g' $output_report
