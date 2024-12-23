$curr_date = Get-Date -Format "dddd_MM_dd_yyyy"

$searchResult = az search query-key create --name "new_query_$curr_date" `
    --service-name "fowlart-ai-search" `
    --resource-group "rg-fowlartChat" | ConvertFrom-Json

$key = $searchResult.key
Write-Host key is>$key

