#!/bin/bash
# Script to create S3 bucket and DynamoDB table for Terraform state
# Run this ONCE before using Terraform with S3 backend

set -e

AWS_REGION="us-east-1"
BUCKET_NAME="overfitting-demo-terraform-state"
DYNAMODB_TABLE="terraform-state-lock"

echo "🚀 Setting up Terraform backend resources..."
echo ""

# Create S3 bucket for Terraform state
echo "📦 Creating S3 bucket: $BUCKET_NAME"
aws s3api create-bucket \
    --bucket $BUCKET_NAME \
    --region $AWS_REGION \
    2>/dev/null || echo "Bucket already exists or error creating bucket"

# Enable versioning on the bucket
echo "🔄 Enabling versioning..."
aws s3api put-bucket-versioning \
    --bucket $BUCKET_NAME \
    --versioning-configuration Status=Enabled \
    --region $AWS_REGION

# Enable encryption
echo "🔒 Enabling encryption..."
aws s3api put-bucket-encryption \
    --bucket $BUCKET_NAME \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }]
    }' \
    --region $AWS_REGION

# Block public access
echo "🛡️  Blocking public access..."
aws s3api put-public-access-block \
    --bucket $BUCKET_NAME \
    --public-access-block-configuration \
        "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true" \
    --region $AWS_REGION

# Create DynamoDB table for state locking
echo "🔐 Creating DynamoDB table: $DYNAMODB_TABLE"
aws dynamodb create-table \
    --table-name $DYNAMODB_TABLE \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region $AWS_REGION \
    2>/dev/null || echo "Table already exists or error creating table"

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "Next steps:"
echo "1. Uncomment the backend block in main.tf"
echo "2. Run: terraform init -migrate-state"
echo "3. Confirm migration when prompted"
