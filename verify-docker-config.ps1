# Verify Docker configuration

Write-Host "🔍 Verifying Docker Configuration" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check .env file
Write-Host "1. Checking .env file..." -ForegroundColor Yellow
if (Test-Path .env) {
    Write-Host "   ✓ .env exists" -ForegroundColor Green
    $envContent = Get-Content .env -Raw
    if ($envContent -match "MCP_ENDPOINT=wss://.*token=") {
        Write-Host "   ✓ MCP_ENDPOINT found" -ForegroundColor Green
        $token = ($envContent | Select-String "token=([^`n]+)").Matches.Groups[1].Value
        if ($token -and $token -ne "YOUR_TOKEN_HERE") {
            Write-Host "   ✓ Token looks valid" -ForegroundColor Green
        } else {
            Write-Host "   ✗ Token is placeholder or empty" -ForegroundColor Red
        }
    } else {
        Write-Host "   ✗ MCP_ENDPOINT not found or invalid" -ForegroundColor Red
    }
} else {
    Write-Host "   ✗ .env file not found" -ForegroundColor Red
}

Write-Host ""

# Check docker-compose.yml
Write-Host "2. Checking docker-compose.yml..." -ForegroundColor Yellow
if (Test-Path docker-compose.yml) {
    Write-Host "   ✓ docker-compose.yml exists" -ForegroundColor Green
    $composeContent = Get-Content docker-compose.yml -Raw
    
    if ($composeContent -match "env_file:") {
        Write-Host "   ✓ env_file configured" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ env_file not configured (using environment variables)" -ForegroundColor Yellow
    }
    
    if ($composeContent -match "MCP_ENDPOINT=\$\{MCP_ENDPOINT\}") {
        Write-Host "   ✓ MCP_ENDPOINT will be loaded from .env" -ForegroundColor Green
    } elseif ($composeContent -match "YOUR_TOKEN_HERE") {
        Write-Host "   ✗ Still using placeholder token!" -ForegroundColor Red
        Write-Host "   Update docker-compose.yml to use: MCP_ENDPOINT=`${MCP_ENDPOINT}" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ✗ docker-compose.yml not found" -ForegroundColor Red
}

Write-Host ""

# Check mcp_config.json
Write-Host "3. Checking mcp_config.json..." -ForegroundColor Yellow
if (Test-Path mcp_config.json) {
    Write-Host "   ✓ mcp_config.json exists" -ForegroundColor Green
    $config = Get-Content mcp_config.json | ConvertFrom-Json
    $serverCount = ($config.mcpServers.PSObject.Properties | Measure-Object).Count
    Write-Host "   Servers configured: $serverCount" -ForegroundColor Gray
    
    if ($serverCount -gt 2) {
        Write-Host "   ⚠ Many servers may cause connection issues" -ForegroundColor Yellow
        Write-Host "   Consider using mcp_config.minimal.json" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ✗ mcp_config.json not found" -ForegroundColor Red
}

Write-Host ""

# Summary
Write-Host "📊 Summary" -ForegroundColor Cyan
Write-Host "==========" -ForegroundColor Cyan
Write-Host ""
Write-Host "Windows vs Docker token comparison:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Windows (local):" -ForegroundColor White
Write-Host "  - Reads from: .env file" -ForegroundColor Gray
Write-Host "  - Token: $(if (Test-Path .env) { 'Valid' } else { 'Missing' })" -ForegroundColor $(if (Test-Path .env) { 'Green' } else { 'Red' })
Write-Host ""
Write-Host "Docker:" -ForegroundColor White
Write-Host "  - Reads from: docker-compose.yml + .env" -ForegroundColor Gray
$dockerToken = if ((Get-Content docker-compose.yml -Raw) -match "env_file:") { "From .env" } else { "From environment" }
Write-Host "  - Token source: $dockerToken" -ForegroundColor Gray
Write-Host ""

if ((Get-Content docker-compose.yml -Raw) -match "YOUR_TOKEN_HERE") {
    Write-Host "⚠️  ISSUE FOUND!" -ForegroundColor Red
    Write-Host "Docker is using placeholder token, not real token from .env" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Fix: Update docker-compose.yml to use:" -ForegroundColor Yellow
    Write-Host "  MCP_ENDPOINT=`${MCP_ENDPOINT}" -ForegroundColor White
} else {
    Write-Host "✅ Configuration looks good!" -ForegroundColor Green
}
