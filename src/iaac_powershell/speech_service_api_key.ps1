$searchResult = az cognitiveservices account keys list --name fowlart-speach-service --resource-group rg-fowlartChat | ConvertFrom-Json
$key = $searchResult.key2
Write-Host $key
Write-Host key is>$key