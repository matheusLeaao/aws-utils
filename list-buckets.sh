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
    if [[ $(echo $policy | jq -r '.Statement | length') -gt 0 ]]; then
        echo "Attached Policy: Yes"
    else
        echo "Attached Policy: No"
    fi
    
    echo
done
