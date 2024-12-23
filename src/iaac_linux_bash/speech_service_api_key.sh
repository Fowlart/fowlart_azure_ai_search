searchResult=$(az cognitiveservices account keys list --name fowlart-speach-service --resource-group rg-fowlartChat)
key=$(echo "$searchResult" | jq -r '.key2')
echo "key is>$key"