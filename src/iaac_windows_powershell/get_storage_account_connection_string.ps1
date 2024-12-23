$searchResult = az storage account show-connection-string -g rg-fowlartChat -n fowlartaisearchstore | ConvertFrom-Json
$connectionString = $searchResult.connectionString
Write-Host connectionString is>$connectionString

