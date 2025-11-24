# Script to compare Docker image sizes (Windows PowerShell)

Write-Host "🔍 Comparing Docker Image Sizes" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Build slim version
Write-Host "📦 Building Slim version (Debian-based)..." -ForegroundColor Yellow
docker-compose build --quiet
$slimInfo = docker images mcp-xiaozhi-vietnam --format "{{.Size}}" | Select-Object -First 1

# Build alpine version
Write-Host "📦 Building Alpine version..." -ForegroundColor Yellow
docker-compose -f docker-compose.alpine.yml build --quiet
$alpineInfo = docker images mcp-xiaozhi-vietnam:alpine --format "{{.Size}}" | Select-Object -First 1

# Display results
Write-Host ""
Write-Host "📊 Results:" -ForegroundColor Cyan
Write-Host "----------" -ForegroundColor Cyan
Write-Host "Slim (Debian):  $slimInfo"
Write-Host "Alpine (Linux): $alpineInfo"
Write-Host ""

# Show detailed info
Write-Host "📋 Detailed Information:" -ForegroundColor Cyan
Write-Host "------------------------" -ForegroundColor Cyan
docker images | Select-String -Pattern "REPOSITORY|mcp-xiaozhi-vietnam"

Write-Host ""
Write-Host "💡 Recommendations:" -ForegroundColor Cyan
Write-Host "-------------------" -ForegroundColor Cyan
Write-Host "- Use Alpine for production (smallest size)"
Write-Host "- Use Slim for development (better compatibility)"
Write-Host ""
Write-Host "To use Alpine version:" -ForegroundColor Yellow
Write-Host "  docker-compose -f docker-compose.alpine.yml up -d"
