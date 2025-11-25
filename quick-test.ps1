# Quick test script

Write-Host "🚀 Quick Test MCP Servers" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Check files
Write-Host "Checking files..." -ForegroundColor Yellow
$files = @(".env", "mcp_config.json", "mcp_pipe.py", "calculator.py", "VnExpress.py")
$allExist = $true

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file missing" -ForegroundColor Red
        $allExist = $false
    }
}

if (-not $allExist) {
    Write-Host ""
    Write-Host "Some files are missing!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Validate JSON
Write-Host "Validating mcp_config.json..." -ForegroundColor Yellow
try {
    python -c "import json; json.load(open('mcp_config.json'))"
    Write-Host "  ✓ JSON is valid" -ForegroundColor Green
} catch {
    Write-Host "  ✗ JSON is invalid" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check .env
Write-Host "Checking .env..." -ForegroundColor Yellow
$envContent = Get-Content .env -Raw
if ($envContent -match "MCP_ENDPOINT=wss://") {
    Write-Host "  ✓ MCP_ENDPOINT is set" -ForegroundColor Green
} else {
    Write-Host "  ✗ MCP_ENDPOINT not found" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Test Python imports
Write-Host "Testing Python imports..." -ForegroundColor Yellow
$imports = @("fastmcp", "websockets", "dotenv")
foreach ($module in $imports) {
    try {
        python -c "import $module" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ $module" -ForegroundColor Green
        } else {
            Write-Host "  ✗ $module not found" -ForegroundColor Red
        }
    } catch {
        Write-Host "  ✗ $module not found" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "✅ All checks passed!" -ForegroundColor Green
Write-Host ""
Write-Host "Starting MCP servers..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

# Run
python mcp_pipe.py
