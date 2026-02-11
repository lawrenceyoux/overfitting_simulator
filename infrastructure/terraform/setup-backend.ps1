# Script to create S3 bucket and DynamoDB table for Terraform state
# Run this ONCE before using Terraform with S3 backend

$ErrorActionPreference = "Continue"

$AWS_REGION = "us-east-1"
$BUCKET_NAME = "overfitting-demo-terraform-state"
$DYNAMODB_TABLE = "terraform-state-lock"

Write-Host "🚀 Setting up Terraform backend resources..." -ForegroundColor Cyan
Write-Host ""

# Create S3 bucket for Terraform state
Write-Host "📦 Creating S3 bucket: $BUCKET_NAME" -ForegroundColor Yellow
try {
    aws s3api create-bucket --bucket $BUCKET_NAME --region $AWS_REGION 2>&1 | Out-Null
    Write-Host "✅ Bucket created successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Bucket already exists or error occurred" -ForegroundColor Yellow
}

# Enable versioning on the bucket
Write-Host "🔄 Enabling versioning..." -ForegroundColor Yellow
aws s3api put-bucket-versioning `
    --bucket $BUCKET_NAME `
    --versioning-configuration Status=Enabled `
    --region $AWS_REGION

# Enable encryption
Write-Host "🔒 Enabling encryption..." -ForegroundColor Yellow
$encryptionConfig = @"
{
    "Rules": [{
        "ApplyServerSideEncryptionByDefault": {
            "SSEAlgorithm": "AES256"
        }
    }]
}
"@

aws s3api put-bucket-encryption `
    --bucket $BUCKET_NAME `
    --server-side-encryption-configuration $encryptionConfig `
    --region $AWS_REGION

# Block public access
Write-Host "🛡️  Blocking public access..." -ForegroundColor Yellow
aws s3api put-public-access-block `
    --bucket $BUCKET_NAME `
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true" `
    --region $AWS_REGION

# Create DynamoDB table for state locking
Write-Host "🔐 Creating DynamoDB table: $DYNAMODB_TABLE" -ForegroundColor Yellow
try {
    aws dynamodb create-table `
        --table-name $DYNAMODB_TABLE `
        --attribute-definitions AttributeName=LockID,AttributeType=S `
        --key-schema AttributeName=LockID,KeyType=HASH `
        --billing-mode PAY_PER_REQUEST `
        --region $AWS_REGION 2>&1 | Out-Null
    Write-Host "✅ DynamoDB table created successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Table already exists or error occurred" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Backend setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Uncomment the backend block in main.tf"
Write-Host "2. Run: terraform init -migrate-state"
Write-Host "3. Confirm migration when prompted"
