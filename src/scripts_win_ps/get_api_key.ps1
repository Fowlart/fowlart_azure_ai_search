# Execute the Azure CLI command and capture the output
$searchResult = az search admin-key show --service-name fowlart-ai-search --resource-group rg-fowlartChat  | ConvertFrom-Json
Write-Host raw response:
$key = $searchResult.primaryKey
Write-Host $key
Write-Host key is>$key


