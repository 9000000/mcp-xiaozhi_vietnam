# Setup script for MCP Xiaozhi Vietnam (Windows PowerShell)
# This script helps you configure and run the Docker containers

Write-Host "🚀 MCP Xiaozhi Vietnam - Setup Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    docker --version | Out-Null
    Write-Host "✓ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "Visit: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
    exit 1
}

# Check if Docker Compose is installed
try {
    docker-compose --version | Out-Null
    Write-Host "✓ Docker Compose is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Ask for MCP token
Write-Host "📝 Configuration" -ForegroundColor Cyan
Write-Host "----------------" -ForegroundColor Cyan
$TOKEN = Read-Host "Enter your MCP token (or press Enter to edit docker-compose.yml manually)"

if ($TOKEN) {
    # Update docker-compose.yml with the token
    $content = Get-Content docker-compose.yml -Raw
    $content = $content -replace 'YOUR_TOKEN_HERE', $TOKEN
    Set-Content docker-compose.yml -Value $content
    Write-Host "✓ Token configured in docker-compose.yml" -ForegroundColor Green
} else {
    Write-Host "⚠️  Please edit docker-compose.yml manually and replace YOUR_TOKEN_HERE with your actual token" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to continue after editing docker-compose.yml"
}

Write-Host ""
Write-Host "🔨 Building Docker image..." -ForegroundColor Cyan
docker-compose build

Write-Host ""
Write-Host "🚀 Starting containers..." -ForegroundColor Cyan
docker-compose up -d

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Useful commands:" -ForegroundColor Cyan
Write-Host "  - View logs:        docker-compose logs -f"
Write-Host "  - Stop containers:  docker-compose down"
Write-Host "  - Restart:          docker-compose restart"
Write-Host "  - View status:      docker-compose ps"
Write-Host ""
Write-Host "📖 For more information, see DOCKER.md" -ForegroundColor Cyan
