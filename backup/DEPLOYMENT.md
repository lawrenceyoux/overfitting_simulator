# AWS Deployment Guide

## Quick Start

### Option 1: AWS Elastic Beanstalk (Easiest)

```bash
# Install EB CLI
pip install awsebcli

# Initialize Elastic Beanstalk
eb init -p docker overfitting-demo --region us-east-1

# Create environment
eb create overfitting-demo-prod --instance-type t3.small

# Deploy
eb deploy

# Open in browser
eb open
```

### Option 2: AWS ECS Fargate (Production-Ready)

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name overfitting-demo --region us-east-1

# 2. Get ECR login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# 3. Build and push Docker image
docker build -t overfitting-demo .
docker tag overfitting-demo:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/overfitting-demo:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/overfitting-demo:latest

# 4. Deploy using Terraform
cd .aws/terraform
terraform init
terraform plan
terraform apply

# 5. Create ECS service (or use console)
aws ecs create-service \
  --cluster overfitting-demo-cluster \
  --service-name streamlit-app-service \
  --task-definition overfitting-demo-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

---

## Prerequisites

1. **AWS Account**: Sign up at aws.amazon.com
2. **AWS CLI**: Install from aws.amazon.com/cli/
3. **Docker**: Install from docker.com
4. **GitHub Account**: For CI/CD pipeline

---

## Setup GitHub Actions CI/CD

### 1. Create AWS IAM User for GitHub Actions

```bash
# Create IAM user
aws iam create-user --user-name github-actions-overfitting-demo

# Attach policies
aws iam attach-user-policy --user-name github-actions-overfitting-demo --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser
aws iam attach-user-policy --user-name github-actions-overfitting-demo --policy-arn arn:aws:iam::aws:policy/AmazonECS_FullAccess

# Create access key
aws iam create-access-key --user-name github-actions-overfitting-demo
```

### 2. Add Secrets to GitHub Repository

Go to: Repository → Settings → Secrets and variables → Actions

Add these secrets:
- `AWS_ACCESS_KEY_ID`: From step 1
- `AWS_SECRET_ACCESS_KEY`: From step 1
- `AWS_ACCOUNT_ID`: Your AWS account ID

### 3. Push to GitHub

```bash
git add .
git commit -m "Add CI/CD pipeline"
git push origin main
```

GitHub Actions will automatically build and deploy!

---

## Infrastructure as Code (Terraform)

### Initialize Terraform

```bash
cd .aws/terraform

# Initialize
terraform init

# Plan (see what will be created)
terraform plan

# Apply (create infrastructure)
terraform apply

# Destroy (when done)
terraform destroy
```

### What Terraform Creates:

- ✅ VPC with public subnets
- ✅ Application Load Balancer
- ✅ ECS Cluster
- ✅ Security Groups
- ✅ IAM Roles
- ✅ CloudWatch Log Groups
- ✅ ECR Repository
- ✅ S3 Bucket

---

## Manual Deployment Steps

### 1. Build Docker Image Locally

```bash
docker build -t overfitting-demo .
docker run -p 8501:8501 overfitting-demo
# Test at http://localhost:8501
```

### 2. Push to ECR

```bash
# Tag
docker tag overfitting-demo:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/overfitting-demo:latest

# Push
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/overfitting-demo:latest
```

### 3. Update ECS Service

```bash
# Force new deployment
aws ecs update-service --cluster overfitting-demo-cluster --service streamlit-app-service --force-new-deployment
```

---

## Monitoring & Logs

### View Logs

```bash
# CloudWatch Logs
aws logs tail /ecs/overfitting-demo --follow

# Or use AWS Console
# CloudWatch → Logs → Log Groups → /ecs/overfitting-demo
```

### Check Service Health

```bash
# ECS Service status
aws ecs describe-services --cluster overfitting-demo-cluster --services streamlit-app-service

# Check ALB target health
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:...
```

---

## Scaling

### Manual Scaling

```bash
# Scale to 3 replicas
aws ecs update-service --cluster overfitting-demo-cluster --service streamlit-app-service --desired-count 3
```

### Auto-Scaling (Application Auto Scaling)

```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/overfitting-demo-cluster/streamlit-app-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 1 \
  --max-capacity 5

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/overfitting-demo-cluster/streamlit-app-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name cpu-scaling \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

---

## Cost Optimization

### Free Tier Eligible Configuration

```yaml
Instance Type: t3.micro (750 hours/month free for 12 months)
Auto-Scaling: Min=1, Max=1 (no scaling)
ALB: First tier free
S3: 5GB free
CloudWatch: 5GB logs free
```

### Estimated Monthly Cost (After Free Tier)

- **t3.small (Beanstalk)**: ~$15-20/month
- **Fargate (0.25 vCPU, 0.5 GB)**: ~$10-15/month
- **ALB**: ~$20/month
- **Data Transfer**: ~$5/month
- **Total**: **$40-60/month**

### How to Minimize Costs

1. Use t3.micro for demo purposes
2. Stop instances when not in use
3. Use Fargate Spot for 70% savings
4. Set up billing alarms

```bash
# Create billing alarm
aws cloudwatch put-metric-alarm \
  --alarm-name monthly-cost-alarm \
  --alarm-description "Alert when monthly cost exceeds $50" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 21600 \
  --evaluation-periods 1 \
  --threshold 50 \
  --comparison-operator GreaterThanThreshold
```

---

## Troubleshooting

### Issue: Container won't start

```bash
# Check ECS task logs
aws ecs describe-tasks --cluster overfitting-demo-cluster --tasks TASK_ID
aws logs tail /ecs/overfitting-demo --follow
```

### Issue: Health checks failing

```bash
# Check target group health
aws elbv2 describe-target-health --target-group-arn ARN

# Test health endpoint locally
docker run -p 8501:8501 overfitting-demo
curl http://localhost:8501/_stcore/health
```

### Issue: 502 Bad Gateway

- Check security group allows traffic on port 8501
- Verify container is listening on 0.0.0.0:8501
- Check CloudWatch logs for errors

---

## Security Best Practices

1. ✅ Use IAM roles (no hardcoded credentials)
2. ✅ Enable HTTPS with ACM certificate
3. ✅ Use private subnets for ECS tasks
4. ✅ Enable CloudTrail for audit logging
5. ✅ Scan Docker images for vulnerabilities
6. ✅ Use Secrets Manager for sensitive data
7. ✅ Enable VPC Flow Logs
8. ✅ Set up WAF for DDoS protection

---

## Custom Domain Setup

### 1. Register Domain (Route 53 or other registrar)

### 2. Create ACM Certificate

```bash
aws acm request-certificate \
  --domain-name overfitting-demo.com \
  --domain-name *.overfitting-demo.com \
  --validation-method DNS
```

### 3. Add HTTPS Listener to ALB

```bash
aws elbv2 create-listener \
  --load-balancer-arn ALB_ARN \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=ACM_CERT_ARN \
  --default-actions Type=forward,TargetGroupArn=TG_ARN
```

### 4. Create Route 53 Record

```bash
# Point domain to ALB
# Create A record (alias) to ALB DNS name
```

---

## Rollback Strategy

### Automatic Rollback (in GitHub Actions)

The CI/CD pipeline includes automatic rollback on failure.

### Manual Rollback

```bash
# List previous task definitions
aws ecs list-task-definitions --family-prefix overfitting-demo-task

# Update service to previous version
aws ecs update-service \
  --cluster overfitting-demo-cluster \
  --service streamlit-app-service \
  --task-definition overfitting-demo-task:PREVIOUS_VERSION
```

---

## Clean Up (Delete Everything)

### Terraform

```bash
cd .aws/terraform
terraform destroy
```

### Manual

```bash
# Delete ECS service
aws ecs delete-service --cluster overfitting-demo-cluster --service streamlit-app-service --force

# Delete ECS cluster
aws ecs delete-cluster --cluster overfitting-demo-cluster

# Delete ECR images and repository
aws ecr batch-delete-image --repository-name overfitting-demo --image-ids imageTag=latest
aws ecr delete-repository --repository-name overfitting-demo

# Delete S3 bucket
aws s3 rb s3://overfitting-demo-data-production --force
```

---

## Additional Resources

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

## Support

For issues:
1. Check CloudWatch Logs
2. Review GitHub Actions logs
3. Consult AWS documentation
4. Open GitHub Issue

**Good luck with your deployment! 🚀**
