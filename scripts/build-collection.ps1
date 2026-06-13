# Build the DeckSafe collection from the latest moxfield export

$latestFile = Get-ChildItem -Path .\collection\moxfield_haves_*.csv -ErrorAction Stop | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $latestFile) {
    Write-Error "No moxfield_haves_*.csv file found in .\collection\"
    exit 1
}

Write-Host "Using: $($latestFile.Name)"
python $env:DECKSAFE_REPO/deck_safe_collection_builder.py $latestFile.FullName --deck-dir .\decks\ -o .\collection\deck_safe_collection.xlsx
