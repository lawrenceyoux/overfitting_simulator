# Terraform Setup Guide

## Prerequisites

1. AWS CLI configured with credentials
2. Terraform installed (v1.5.0+)
3. GitHub Secrets configured:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

## 🚀 First-Time Setup

### Step 1: Create Terraform Backend (One-Time)

The Terraform backend stores the state file in S3 and uses DynamoDB for state locking.

**On Windows:**
```powershell
cd infrastructure/terraform
.\setup-backend.ps1
```

**On Linux/Mac:**
```bash
cd infrastructure/terraform
chmod +x setup-backend.sh
./setup-backend.sh
```

This creates:
- S3 bucket: `overfitting-demo-terraform-state`
- DynamoDB table: `terraform-state-lock`

### Step 2: Enable Remote Backend

After running the setup script, uncomment the backend block in `main.tf`:

```terraform
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "overfitting-demo-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### Step 3: Initialize Terraform

```bash
terraform init -migrate-state
```

Terraform will ask to migrate your local state to S3. Type `yes`.

### Step 4: Deploy Infrastructure

**Option A: Via GitHub Actions (Recommended)**
1. Push the terraform code to your repository
2. Go to GitHub → Actions → "Deploy Infrastructure"
3. Click "Run workflow"
4. Select action: "apply"
5. Click "Run workflow"

**Option B: Locally**
```bash
terraform plan
terraform apply
```

## 📋 What Gets Created

- **VPC** with public subnets across 2 AZs
- **Application Load Balancer** (ALB)
- **ECS Cluster** for running containers
- **ECR Repository** for Docker images
- **S3 Buckets** for data storage
- **IAM Roles** with appropriate permissions
- **Security Groups** for network access
- **CloudWatch Log Groups** for monitoring

## 🔄 Workflow Integration

After infrastructure is deployed:

1. **deploy-infrastructure.yml** - Only runs when you modify `infrastructure/terraform/**`
2. **pipeline.yml** - Builds and deploys your app on every push to `main`/`develop`
3. **deploy-lambda.yml** - Deploys Lambda functions when you modify Lambda code

## 🧹 Cleanup

To destroy all infrastructure:

1. Go to GitHub → Actions → "Deploy Infrastructure"
2. Run workflow with action: "destroy"

Or locally:
```bash
terraform destroy
```

To remove the backend resources:
```bash
aws s3 rb s3://overfitting-demo-terraform-state --force
aws dynamodb delete-table --table-name terraform-state-lock --region us-east-1
```

## 💡 Tips

- **First deployment**: Takes ~10-15 minutes
- **State file**: Always stored in S3, never commit `terraform.tfstate` to git
- **Costs**: Running this infrastructure costs ~$50-100/month (ALB, ECS, etc.)
- **Testing changes**: Use `terraform plan` first to see what will change

## 🆘 Troubleshooting

**"Backend initialization required"**
- Run `terraform init`

**"Error acquiring the state lock"**
- Another terraform process is running, wait for it to finish
- Or force unlock: `terraform force-unlock <lock-id>`

**"Insufficient permissions"**
- Ensure your AWS credentials have admin or appropriate IAM permissions

**"Bucket already exists"**
- If the bucket name is taken globally, change `BUCKET_NAME` in setup scripts and `main.tf`
