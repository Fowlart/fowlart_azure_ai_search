curr_date=$(date +"%A_%m_%d_%Y")

az deployment group create --name $curr_date /
    --resource-group "rg-fowlartChat" /
    --template-file "./speech_service.json"