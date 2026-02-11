# PowerShell script to package Lambda functions for deployment

$ErrorActionPreference = "Stop"

$ScriptDir = $PSScriptRoot
$LambdaDir = $ScriptDir
$BuildDir = Join-Path $ScriptDir "build"
$OutputZip = Join-Path $ScriptDir "lambda_package.zip"

Write-Host "Building Lambda deployment package..." -ForegroundColor Green

# Clean previous build
if (Test-Path $BuildDir) {
    Remove-Item $BuildDir -Recurse -Force
}
if (Test-Path $OutputZip) {
    Remove-Item $OutputZip -Force
}

# Create build directory
New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null

# Copy Lambda function files
Write-Host "Copying Lambda functions..." -ForegroundColor Yellow
Get-ChildItem -Path $LambdaDir -Filter "*.py" | Copy-Item -Destination $BuildDir

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
$RequirementsFile = Join-Path $LambdaDir "requirements.txt"
if (Test-Path $RequirementsFile) {
    pip install -r $RequirementsFile -t $BuildDir --upgrade --quiet
}

# Create zip package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
Compress-Archive -Path "$BuildDir\*" -DestinationPath $OutputZip -Force

# Clean up
Remove-Item $BuildDir -Recurse -Force

Write-Host "Lambda package created: $OutputZip" -ForegroundColor Green
$Size = (Get-Item $OutputZip).Length / 1MB
Write-Host ("Package size: {0:N2} MB" -f $Size) -ForegroundColor Green
