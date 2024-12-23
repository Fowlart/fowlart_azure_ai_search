#!/bin/bash

# Get the current date in the format "dddd_MM_dd_yyyy"
curr_date=$(date +"%A_%m_%d_%Y")

# Execute the Azure CLI command and capture the output
searchResult=$(az search query-key create \
    --name "new_query_$curr_date" \
    --service-name "fowlart-ai-search" \
    --resource-group "rg-fowlartChat" \
    --output json)

# Extract the key value from the JSON output
key=$(echo "$searchResult" | jq -r '.key')

# Print the key
echo "key is: $key"