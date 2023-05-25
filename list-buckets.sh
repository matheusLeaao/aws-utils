#!/bin/bash

# Lista os buckets S3
buckets=$(aws s3api list-buckets --query "Buckets[].Name" --output text)

# Loop pelos buckets
for bucket in $buckets; do
    echo "Bucket: $bucket"
    
    # Obtém a configuração do lifecycle
    lifecycle=$(aws s3api get-bucket-lifecycle-configuration --bucket $bucket --output json 2>/dev/null)
    
    # Verifica se existe uma política de lifecycle
    if [[ $(echo $lifecycle | jq -r '.Rules | length') -gt 0 ]]; then
        # Obtém o nome da política de lifecycle
        policy_name=$(echo $lifecycle | jq -r '.Rules[0].ID')
        echo "Política de Lifecycle: $policy_name"
    else
        echo "Nenhuma política de Lifecycle definida"
    fi
    
    echo
done
