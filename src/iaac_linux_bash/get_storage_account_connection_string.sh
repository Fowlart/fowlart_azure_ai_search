searchResult=$(az storage account show-connection-string -g rg-fowlartChat -n fowlartaisearchstore)
key=$(echo "$searchResult" | jq -r '.connectionString')
echo "connectionString is>$key"

