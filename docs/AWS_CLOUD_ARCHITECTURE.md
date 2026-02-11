# AWS Cloud Architecture - Full Production Setup

## 🏗️ Architecture Overview

This project now features a **complete serverless data pipeline** running entirely in AWS cloud. All data processing happens in AWS, with results stored in S3 and served dynamically by the Streamlit application.

```
┌─────────────────────────────────────────────────────────────────┐
│                         GitHub Actions                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Deploy Lambda│  │  Deploy ECS  │  │  Trigger Pipeline    │  │
│  │  Functions   │  │     App      │  │   (Manual)           │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────────────┘  │
└─────────┼──────────────────┼──────────────────┼──────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                          AWS Cloud                              │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Step Functions Orchestration                │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────┐│  │
│  │  │Generate│→ │Backtest│→ │ Select │→ │Validate│→ │ Viz││  │
│  │  │Strats  │  │        │  │  Best  │  │        │  │    ││  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘  └────┘│  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                           │
│                     ▼                                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    S3 Bucket                             │  │
│  │  ├── raw/btc_price_data.csv                             │  │
│  │  ├── strategies/strategies_latest.json                  │  │
│  │  ├── results/                                           │  │
│  │  │   ├── training_performance.csv                      │  │
│  │  │   ├── best_strategy.json                            │  │
│  │  │   └── validation_results.json                       │  │
│  │  └── plots/                                             │  │
│  │      ├── win_rate_histogram.png                         │  │
│  │      └── performance_comparison.png                     │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                           │
│                     ▼                                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │               ECS Fargate (Streamlit App)               │  │
│  │    ┌─────────────────────────────────────────┐          │  │
│  │    │  Reads from S3 → Displays Results       │          │  │
│  │    └─────────────────────────────────────────┘          │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                           │
└─────────────────────┼───────────────────────────────────────────┘
                      │
                      ▼
                 [End Users]
```

## 📦 AWS Services Used

### Compute
- **AWS Lambda** (5 functions): Serverless data processing
  - `generate-strategies`: Creates 500 random trading strategies
  - `backtest-strategies`: Tests strategies on training data
  - `select-best`: Identifies top performer
  - `validate-strategy`: Tests on validation data (exposes overfitting)
  - `visualize`: Generates charts and plots

- **ECS Fargate**: Runs Streamlit web application (serverless containers)

### Orchestration
- **Step Functions**: Chains Lambda functions into a complete pipeline
  - Automatic retries on failures
  - Error handling and logging
  - State management between steps

### Storage
- **S3**: Central data lake for all inputs/outputs
  - Versioning enabled
  - Server-side encryption (AES-256)
  - Organized folder structure

### Networking
- **VPC**: Custom network (10.0.0.0/16)
- **Application Load Balancer**: HTTPS endpoint for Streamlit app
- **Security Groups**: Firewall rules for ALB → ECS communication

### Monitoring
- **CloudWatch Logs**: Centralized logging for all services
- **CloudWatch Metrics**: Performance monitoring
- **Container Insights**: ECS cluster metrics

### CI/CD
- **GitHub Actions**: Automated deployment pipelines
  - Lambda deployment workflow
  - ECS app deployment workflow
  - Manual pipeline trigger workflow

## 🚀 Deployment Guide

### Prerequisites
1. AWS Account with credentials configured
2. GitHub repository with secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
3. S3 bucket for Terraform state: `overfitting-demo-terraform-state`
4. DynamoDB table for state locking: `terraform-state-lock`

### Step 1: Deploy Infrastructure (One-time Setup)

```bash
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Deploy all infrastructure
terraform apply
```

This creates:
- VPC, Subnets, Internet Gateway, Load Balancer
- S3 bucket for data
- ECR repository for Docker images
- ECS cluster
- All IAM roles

### Step 2: Build and Deploy Lambda Functions

**Option A: GitHub Actions (Recommended)**
1. Push code to GitHub
2. Workflow `deploy-lambda.yml` runs automatically
3. Builds Lambda package and deploys via Terraform

**Option B: Manual Deployment**
```bash
cd infrastructure/lambda

# Build Lambda package
./build_lambda_package.ps1  # Windows
# OR
./build_lambda_package.sh   # Linux/Mac

# Deploy with Terraform
cd ../terraform
terraform apply -target=module.lambda
```

### Step 3: Upload Initial Data to S3

```bash
# Get S3 bucket name from Terraform
S3_BUCKET=$(cd infrastructure/terraform && terraform output -raw s3_bucket_name)

# Upload Bitcoin price data
aws s3 cp data/btc_price_data.csv s3://$S3_BUCKET/raw/btc_price_data.csv
```

### Step 4: Deploy Streamlit Application

**Via GitHub Actions:**
1. Push code changes
2. Workflow `pipeline.yml` runs automatically:
   - Builds Docker image
   - Pushes to ECR
   - Updates ECS service
   - Deploys to production

**Manual Docker Build:**
```bash
# Build and tag
docker build -f infrastructure/docker/Dockerfile -t overfitting-demo .

# Tag for ECR
ECR_URI=$(cd infrastructure/terraform && terraform output -raw ecr_repository_url)
docker tag overfitting-demo:latest $ECR_URI:latest

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_URI
docker push $ECR_URI:latest

# Update ECS service (force new deployment)
aws ecs update-service \
  --cluster overfitting-demo-cluster \
  --service streamlit-app-service \
  --force-new-deployment
```

## 🎯 Running the Data Pipeline

### Manual Trigger via GitHub Actions (Easiest)

1. Go to GitHub → Actions → "Run Data Pipeline"
2. Click "Run workflow"
3. Enter number of strategies (default: 500)
4. Click "Run workflow" button
5. Wait for completion (~5-10 minutes)
6. View results in summary

### Manual Trigger via AWS CLI

```bash
# Get Step Functions ARN
SF_ARN=$(cd infrastructure/terraform && terraform output -raw step_functions_arn)

# Start execution
aws stepfunctions start-execution \
  --state-machine-arn "$SF_ARN" \
  --name "pipeline-run-$(date +%Y%m%d-%H%M%S)" \
  --input '{"bucket": "overfitting-demo-data-production", "num_strategies": 500}'

# Monitor execution
aws stepfunctions describe-execution --execution-arn <EXECUTION_ARN>
```

### Manual Trigger via AWS Console

1. Open AWS Console → Step Functions
2. Find `overfitting-demo-data-pipeline`
3. Click "Start execution"
4. Enter JSON input:
   ```json
   {
     "bucket": "overfitting-demo-data-production",
     "num_strategies": 500
   }
   ```
5. Click "Start execution"
6. Monitor progress in visual workflow

## 📊 Pipeline Execution Flow

```
1. Generate Strategies (Lambda 1)
   ├─ Creates 500 random strategies
   ├─ Saves to S3: strategies/strategies_latest.json
   └─ Passes bucket + key to next step

2. Backtest Strategies (Lambda 2)
   ├─ Reads strategies from S3
   ├─ Reads price data from S3
   ├─ Tests each strategy on training data (70%)
   ├─ Calculates win rate, Sharpe, drawdown
   └─ Saves results/training_performance.csv to S3

3. Select Best Strategy (Lambda 3)
   ├─ Reads backtest results from S3
   ├─ Identifies highest win rate
   ├─ Saves results/best_strategy.json to S3
   └─ Passes best strategy details

4. Validate Strategy (Lambda 4)
   ├─ Reads best strategy from S3
   ├─ Tests on validation data (30%)
   ├─ Compares training vs validation performance
   ├─ Saves results/validation_results.json to S3
   └─ Detects overfitting (>15% performance drop)

5. Generate Visualizations (Lambda 5)
   ├─ Reads backtest + validation results
   ├─ Creates win rate histogram
   ├─ Creates performance comparison chart
   └─ Saves PNG images to S3: plots/

6. Complete
   └─ Returns summary JSON with all metrics
```

## 💰 Cost Estimate

### Monthly Costs (assuming moderate usage)

| Service | Usage | Cost/Month |
|---------|-------|------------|
| Lambda (5 functions) | 100 runs @ 2 min avg | $2-5 |
| Step Functions | 100 executions | $0.25 |
| S3 Storage | 1 GB | $0.023 |
| S3 Requests | 10,000 GET | $0.004 |
| ECS Fargate | 1 task, 24/7, 0.5 vCPU, 1 GB | $15-20 |
| ALB | 1 ALB, 24/7 | $16 |
| CloudWatch Logs | 5 GB | $2.50 |
| Data Transfer | 10 GB out | $0.90 |
| **Total** | | **~$37-45/month** |

### Cost Optimization Tips
- **Stop ECS task when not demoing** → Save $15-20/month
- **Use CloudWatch log retention** → Auto-delete old logs
- **S3 Lifecycle policies** → Archive old results to Glacier
- **Lambda memory optimization** → Reduce to 512 MB if possible

## 🔒 Security Best Practices

### Implemented
✅ **IAM Least Privilege**: Each service has minimal required permissions
✅ **S3 Encryption**: Server-side encryption enabled (AES-256)
✅ **VPC Security Groups**: ALB can only talk to ECS on port 8501
✅ **Container Security**: Non-root user in Docker container
✅ **Secrets Management**: AWS credentials via GitHub Secrets
✅ **CloudWatch Logging**: All services log to CloudWatch

### Production Enhancements
- [ ] Enable HTTPS on ALB (requires ACM certificate)
- [ ] Add WAF rules for DDoS protection
- [ ] Enable VPC Flow Logs
- [ ] Add S3 bucket policies for cross-account access prevention
- [ ] Enable GuardDuty for threat detection
- [ ] Use AWS Secrets Manager for API keys

## 📈 Monitoring & Troubleshooting

### CloudWatch Dashboards

Monitor key metrics:
```bash
# Lambda Errors
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=overfitting-demo-generate-strategies \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum

# ECS CPU Usage
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ServiceName,Value=streamlit-app-service Name=ClusterName,Value=overfitting-demo-cluster \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average
```

### Common Issues

**Q: Step Functions execution fails on Lambda timeout**
```bash
# Increase Lambda timeout in Terraform
# lambda.tf → timeout = 600 (10 minutes)
terraform apply
```

**Q: Streamlit app shows "No data available"**
```bash
# Verify data exists in S3
aws s3 ls s3://overfitting-demo-data-production/results/

# Check ECS task environment variables
aws ecs describe-task-definition --task-definition overfitting-demo-task \
  | jq '.taskDefinition.containerDefinitions[0].environment'

# Should show USE_S3=true and correct S3_BUCKET
```

**Q: Lambda can't access S3**
```bash
# Verify IAM role has S3 permissions
aws iam get-role-policy \
  --role-name overfitting-demo-lambda-execution-role \
  --policy-name overfitting-demo-lambda-s3-policy
```

## 🔄 Development Workflow

### Local Development (Without AWS)
```bash
# Set environment to use local files
export USE_S3=false

# Run Streamlit locally
streamlit run src/app.py

# Generate data locally
python scripts/01_generate_strategies.py
python scripts/02_backtest_strategies.py
```

### Cloud Development (With AWS)
```bash
# Set environment to use S3
export USE_S3=true
export S3_BUCKET=overfitting-demo-data-production
export AWS_REGION=us-east-1

# Run Streamlit locally (reads from S3)
streamlit run src/app.py
```

### Testing Pipeline Locally
```bash
# Invoke Lambda locally with AWS SAM
cd infrastructure/lambda
sam local invoke GenerateStrategiesFunction --event test-event.json
```

## 🎓 Learning Outcomes & Skills Demonstrated

This architecture demonstrates expertise in:

### Cloud Architecture
- ✅ Serverless design patterns
- ✅ Event-driven architecture
- ✅ Microservices separation of concerns
- ✅ Infrastructure as Code (Terraform)

### DevOps & CI/CD
- ✅ GitHub Actions workflows
- ✅ Multi-stage Docker builds
- ✅ Automated testing and deployment
- ✅ Blue/green deployments (ECS)

### AWS Services
- ✅ Lambda, Step Functions, S3, ECS, ECR
- ✅ VPC, ALB, Security Groups
- ✅ CloudWatch, IAM
- ✅ Service integration and orchestration

### Software Engineering
- ✅ Python packaging and modularity
- ✅ Environment-based configuration
- ✅ Error handling and retries
- ✅ Logging and observability

---

**Next Steps**: See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.
