#!/bin/bash
### Run as gsysadmin on 38.130 server

bucket=$1
AWSPATH="/home/gsysadmin/.local/bin/"

set -e

echo "Removing all versions from $bucket"

versions=`"$AWSPATH"aws s3api list-object-versions --bucket $bucket |jq '.Versions | .[] | select(.IsLatest | not)'`
markers=`"$AWSPATH"aws s3api list-object-versions --bucket $bucket |jq '.DeleteMarkers'`

echo "removing files"
for version in $(echo "${versions}" | jq -r '@base64'); do
    version=$(echo ${version} | base64 --decode)

    key=`echo $version | jq -r .Key`
    versionId=`echo $version | jq -r .VersionId `
    cmd=""$AWSPATH"aws s3api delete-object --bucket $bucket --key $key --version-id $versionId"
    echo $cmd
    $cmd
done

echo "removing delete markers"
for marker in $(echo "${markers}" | jq -r '.[] | @base64'); do
    marker=$(echo ${marker} | base64 --decode)

    key=`echo $marker | jq -r .Key`
    versionId=`echo $marker | jq -r .VersionId `
    cmd=""$AWSPATH"aws s3api delete-object --bucket $bucket --key $key --version-id $versionId"
    echo $cmd
    $cmd
done

