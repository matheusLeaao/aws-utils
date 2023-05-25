#!/bin/bash

buckets=$(aws s3api list-buckets --query "Buckets[].Name" --output text)

for bucket in $buckets; do
    echo "Bucket: $bucket"
    
    lifecycle=$(aws s3api get-bucket-lifecycle-configuration --bucket $bucket --output json 2>/dev/null)
    
    if [[ $(echo $lifecycle | jq -r '.Rules | length') -gt 0 ]]; then
        policy_name=$(echo $lifecycle | jq -r '.Rules[0].ID')
        retention_days=$(echo $lifecycle | jq -r '.Rules[0].Expiration.Days')
        echo "Lifecycle Policy: $policy_name (Retention: $retention_days days)"
    else
        echo "No Lifecycle policy defined"
    fi

    policy=$(aws s3api get-bucket-policy --bucket $bucket --output json 2>/dev/null)
    if [[ $(echo $policy | jq -r '.Policy | length') -gt 0 ]]; then
        echo "Attached Policy: Yes"
    else
        echo "Attached Policy: No"
    fi

    objects=$(aws s3api list-objects --bucket $bucket --output json --query "[length(Contents[])]" 2>/dev/null)
    size=$(aws s3api list-objects --bucket $bucket --output json --query "Contents[].Size" 2>/dev/null | awk '{s+=$1} END {print s/1024/1024/1024}') # Tamanho em GB
    echo "Count of Objects: $objects"
    echo "Size: $size GB"
    
    echo
done
