# Check Docker build context

Write-Host "🔍 Checking Docker Build Context" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# List files that will be included
Write-Host "Files that will be copied to Docker:" -ForegroundColor Yellow
Write-Host ""

$files = Get-ChildItem -File -Recurse | Where-Object {
    $path = $_.FullName
    $relativePath = $path.Replace((Get-Location).Path + "\", "")
    
    # Check against .dockerignore patterns
    $ignore = $false
    
    # Read .dockerignore
    if (Test-Path .dockerignore) {
        $patterns = Get-Content .dockerignore | Where-Object { 
            $_ -and -not $_.StartsWith("#") 
        }
        
        foreach ($pattern in $patterns) {
            if ($relativePath -like $pattern -or $relativePath -like "*\$pattern") {
                $ignore = $true
                break
            }
        }
    }
    
    -not $ignore
}

$totalSize = ($files | Measure-Object -Property Length -Sum).Sum
$fileCount = $files.Count

Write-Host "Total files: $fileCount" -ForegroundColor Green
Write-Host "Total size: $([math]::Round($totalSize/1MB, 2)) MB" -ForegroundColor Green
Write-Host ""

Write-Host "Files included:" -ForegroundColor Yellow
$files | ForEach-Object {
    $size = [math]::Round($_.Length/1KB, 2)
    Write-Host "  $($_.Name) ($size KB)" -ForegroundColor Gray
}
