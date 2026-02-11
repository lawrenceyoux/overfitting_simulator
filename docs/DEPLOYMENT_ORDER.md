# 🚀 Deployment Guide - Complete Order

## 📋 Overview of All Workflows

You have **4 GitHub Actions workflows**. Here's what each does:

| # | Workflow | Purpose | What It Creates/Does |
|---|----------|---------|---------------------|
| 1 | **Deploy Infrastructure** | Core AWS infrastructure | VPC, ECR, ECS, S3, Load Balancer, IAM roles |
| 2 | **Deploy Lambda Pipeline** | Lambda data processing infrastructure | 5 Lambda functions, Step Functions state machine |
| 3 | **CI/CD Pipeline** | Build & deploy Streamlit app | Docker image → ECR → ECS deployment |
| 4 | **Run Data Pipeline** | Execute the Lambda pipeline | Triggers Step Functions to run strategy backtesting |

---

## ✅ Complete Deployment Order

### 🎯 First Time Setup

```
1. Deploy Infrastructure (REQUIRED - Core foundation)
   ├─ Creates: VPC, Subnets, ECR, ECS Cluster, S3 Buckets, ALB
   ├─ Time: ~10-15 minutes
   └─ Manual: GitHub → Actions → "Deploy Infrastructure" → "apply"

2. Deploy Lambda Pipeline (OPTIONAL - Only if you want data pipeline)
   ├─ Creates: Lambda functions, Step Functions
   ├─ Requires: Step 1 completed (needs S3 bucket)
   ├─ Time: ~3-5 minutes
   └─ Manual: GitHub → Actions → "Deploy Lambda Pipeline"

3. CI/CD Pipeline (REQUIRED - Deploy your app)
   ├─ Builds Docker image, pushes to ECR, deploys to ECS
   ├─ Requires: Step 1 completed (needs ECR)
   ├─ Time: ~5-10 minutes
   └─ Manual: GitHub → Actions → "CI/CD Pipeline"

4. Run Data Pipeline (OPTIONAL - Execute backtesting)
   ├─ Triggers Step Functions to run all Lambda functions
   ├─ Requires: Step 2 completed (Lambda functions must exist)
   ├─ Time: ~10-30 minutes (depends on number of strategies)
   └─ Manual: GitHub → Actions → "Run Data Pipeline"
```

---

## 🤔 Why Are Lambda Functions in a Separate Workflow?

**Good question!** Here's why:

### Terraform in `deploy-lambda.yml`:
- **Purpose**: Creates Lambda infrastructure (functions, Step Functions, IAM roles)
- **Why separate?**: 
  - ✅ **Optional component** - You might not need the data pipeline
  - ✅ **Different update frequency** - Lambda code changes more often than core infra
  - ✅ **Dependency order** - Needs S3 bucket from main infrastructure first
  - ✅ **Cleaner organization** - Separates compute types (ECS vs Lambda)

### Could it be in main infrastructure?
Yes! You could merge them, but keeping them separate:
- Makes each deployment faster
- Reduces risk (changing Lambda won't affect VPC/ECS)
- Allows independent updates

---

## 📊 Detailed Workflow Breakdown

### 1️⃣ Deploy Infrastructure
**File**: `.github/workflows/deploy-infrastructure.yml`  
**Terraform**: `infrastructure/terraform/main.tf`

Creates:
- VPC with public subnets (2 AZs)
- Internet Gateway, Route Tables
- Application Load Balancer (ALB)
- ECS Cluster
- ECR Repository (`overfitting-demo`)
- S3 Bucket (`overfitting-demo-data`)
- IAM Roles (ECS task execution, ECS task)
- Security Groups
- CloudWatch Log Groups

**When to run**: Once initially, then only when infrastructure changes

---

### 2️⃣ Deploy Lambda Pipeline
**File**: `.github/workflows/deploy-lambda.yml`  
**Terraform**: `infrastructure/terraform/lambda-pipeline/` 

Creates:
- **5 Lambda Functions**:
  1. `generate-strategies` - Creates random trading strategies
  2. `backtest-strategies` - Tests strategies on historical data
  3. `select-best` - Picks top performer
  4. `validate-strategy` - Validates on holdout data
  5. `visualize` - Creates performance charts
- **Step Functions State Machine** - Orchestrates all Lambdas
- **IAM Roles** - Lambda execution permissions

**When to run**: After infrastructure, before running data pipeline

---

### 3️⃣ CI/CD Pipeline
**File**: `.github/workflows/pipeline.yml`

Does:
- Code quality checks (black, flake8, pylint)
- Unit tests (pytest)
- Build Docker image
- Push to ECR
- Deploy to ECS
- Update running service

**When to run**: Whenever you update your Streamlit app code

---

### 4️⃣ Run Data Pipeline
**File**: `.github/workflows/run-pipeline.yml`

Does:
- Gets Step Functions ARN from Terraform outputs
- Triggers execution with parameters (num_strategies)
- Waits for completion
- Downloads results from S3
- Displays summary

**When to run**: Whenever you want to run backtesting simulation

---

## 🎮 Quick Start Commands

### Option A: GitHub UI (Easiest)
1. Go to **GitHub** → **Actions**
2. Select workflow from left sidebar
3. Click **"Run workflow"** button
4. Select options (if any)
5. Click **"Run workflow"** to execute

### Option B: GitHub CLI
```bash
# 1. Deploy infrastructure
gh workflow run deploy-infrastructure.yml --ref main \
  -f action=apply

# 2. Deploy Lambda pipeline (optional)
gh workflow run deploy-lambda.yml --ref main

# 3. Deploy app
gh workflow run pipeline.yml --ref main

# 4. Run data pipeline (optional)
gh workflow run run-pipeline.yml --ref main \
  -f num_strategies=500
```

---

## 🔄 Typical Workflow

**Initial Setup** (Do once):
```
Deploy Infrastructure → Deploy Lambda Pipeline → CI/CD Pipeline
```

**Regular Development** (Daily/Weekly):
```
Make code changes → Run CI/CD Pipeline
```

**Run Backtesting** (As needed):
```
Run Data Pipeline (with desired parameters)
```

**Infrastructure Updates** (Rarely):
```
Modify terraform → Deploy Infrastructure
```

---

## 💡 Pro Tips

1. **All workflows are now manual-only** - No automatic triggers on push
2. **You can re-enable auto-triggers** by uncommenting the `push:` section in each workflow
3. **Check dependencies**: Don't run CI/CD before infrastructure exists
4. **Monitor costs**: Running infrastructure costs ~$50-100/month
5. **Destroy when done**: Use infrastructure workflow with `destroy` action

---

## 🆘 Troubleshooting

**"ECR repository doesn't exist"**
→ Run Deploy Infrastructure first

**"S3 bucket not found"**
→ Run Deploy Infrastructure first

**"Step Functions ARN not found"**
→ Run Deploy Lambda Pipeline first

**"No tasks in ECS service"**
→ Run CI/CD Pipeline to deploy app

---

## 📝 Summary

**Minimum to get app running**:
1. Deploy Infrastructure ✅
2. CI/CD Pipeline ✅

**Full data pipeline**:
1. Deploy Infrastructure ✅
2. Deploy Lambda Pipeline ✅
3. CI/CD Pipeline ✅
4. Run Data Pipeline ✅
