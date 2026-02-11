# 🏗️ System Architecture & Design

## Overview

This document outlines the complete architecture for the **Overfitting Demo in Algorithmic Trading** application - designed to showcase development, DevOps, cloud, quantitative analysis, and software engineering skills for potential employers.

---

## 🎯 Project Goals

### Business Objectives
- Demonstrate how easily overfitting occurs in algorithmic trading
- Educate traders/analysts about the dangers of data mining bias
- Provide interactive visualization of statistical concepts

### Technical Objectives
- Showcase full-stack development capabilities
- Demonstrate cloud deployment expertise (AWS)
- Implement modern CI/CD practices
- Display quantitative finance/algorithmic trading knowledge
- Show best practices in software engineering

---

## 🏛️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Browser    │    │  Mobile Web  │    │  Recruiters  │     │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘     │
│         │                   │                    │              │
│         └───────────────────┴────────────────────┘              │
│                             │                                    │
└─────────────────────────────┼────────────────────────────────────┘
                              │
                              │ HTTPS
                              │
┌─────────────────────────────▼────────────────────────────────────┐
│                     AWS CLOUD (us-east-1)                        │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Application Layer                        │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │        AWS Elastic Beanstalk / ECS Fargate         │  │  │
│  │  │                                                     │  │  │
│  │  │    ┌──────────────┐         ┌──────────────┐      │  │  │
│  │  │    │  Container 1 │         │  Container 2 │      │  │  │
│  │  │    │              │         │              │      │  │  │
│  │  │    │  Streamlit   │◄────────┤  Streamlit   │      │  │  │
│  │  │    │     App      │ Auto-   │     App      │      │  │  │
│  │  │    │              │ Scale   │              │      │  │  │
│  │  │    └──────┬───────┘         └──────┬───────┘      │  │  │
│  │  │           │                        │              │  │  │
│  │  └───────────┼────────────────────────┼──────────────┘  │  │
│  │              │                        │                 │  │
│  └──────────────┼────────────────────────┼─────────────────┘  │
│                 │                        │                    │
│  ┌──────────────▼────────────────────────▼─────────────────┐  │
│  │                 Data Layer                               │  │
│  │                                                           │  │
│  │  ┌─────────────┐    ┌──────────────┐   ┌─────────────┐  │  │
│  │  │     S3      │    │  CloudWatch  │   │  DynamoDB   │  │  │
│  │  │             │    │              │   │  (optional) │  │  │
│  │  │  - Results  │    │  - Logs      │   │             │  │  │
│  │  │  - Data     │    │  - Metrics   │   │  - Session  │  │  │
│  │  │  - Plots    │    │  - Alarms    │   │  - Cache    │  │  │
│  │  └─────────────┘    └──────────────┘   └─────────────┘  │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Security & Networking Layer                   │  │
│  │                                                            │  │
│  │  ┌──────────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │   ALB    │  │   VPC   │  │    IAM   │  │  Route53 │  │  │
│  │  │          │  │         │  │          │  │          │  │  │
│  │  │  Load    │  │ Private │  │  Roles & │  │   DNS    │  │  │
│  │  │ Balancer │  │ Subnets │  │ Policies │  │          │  │  │
│  │  └──────────┘  └─────────┘  └──────────┘  └──────────┘  │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      CI/CD PIPELINE                              │
│                                                                   │
│  ┌────────────┐   ┌─────────────┐   ┌──────────────┐           │
│  │   GitHub   │──▶│GitHub Actions│──▶│    AWS ECR   │           │
│  │            │   │              │   │              │           │
│  │  - Code    │   │ - Test       │   │ Docker Images│           │
│  │  - Tests   │   │ - Build      │   │              │           │
│  │  - Config  │   │ - Deploy     │   └──────┬───────┘           │
│  └────────────┘   └──────────────┘          │                   │
│                                              │                   │
│                                  ┌───────────▼────────────┐      │
│                                  │  Auto Deploy to ECS    │      │
│                                  │  or Elastic Beanstalk  │      │
│                                  └────────────────────────┘      │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## 📦 Component Architecture

### 1. Frontend Application (Streamlit)

**Technology Stack:**
- **Framework**: Streamlit (Python web framework)
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Data Processing**: Pandas, NumPy

**Components:**
```
app.py
├── Page Router
│   ├── Overview Page
│   ├── Interactive Demo
│   ├── Real Data Results
│   ├── Deep Dive Analysis
│   └── Educational Content
│
├── Data Layer
│   ├── Cached data loaders
│   ├── JSON parsers
│   └── CSV readers
│
├── Visualization Engine
│   ├── Interactive charts (Plotly)
│   ├── Static plots (Matplotlib)
│   └── Statistical displays
│
└── Business Logic
    ├── Live simulation engine
    ├── Metrics calculator
    └── Statistical analysis
```

### 2. Backend Processing Pipeline

**Batch Processing Scripts:**
```
01_generate_random_strategies.py    # Strategy generation
02_backtest_strategies.py           # Backtesting engine
03_select_best_strategy.py          # Selection logic
04_validate_strategy.py             # Validation testing
05_visualize_results.py             # Static plot generation
```

**Flow:**
```
BTC Data → Generate Strategies → Backtest → Select Best → Validate → Visualize
                                      ↓
                              Training Results
                                      ↓
                              Validation Results
                                      ↓
                              Overfitting Proof
```

### 3. Data Architecture

**Data Flow:**
```
Input Data (Bitcoin OHLCV)
    ↓
Split: 70% Train / 30% Validation
    ↓
Generate 100 Random Strategies
    ↓
Backtest on Training Data
    ↓
Select Best Performers
    ↓
Test on Validation Data
    ↓
Store Results (JSON/CSV)
    ↓
Visualize in Streamlit
```

**Storage Structure:**
```
data/
├── btc_price_data.csv              # Processed BTC data
├── BTCUSD_Candlestick_*.csv        # Raw market data
├── strategies.json                  # Generated strategies
└── synthetic_price_data.csv         # Alternative synthetic data

results/
├── training_performance.csv         # All strategies on train
├── best_strategy.json              # Winner selection
├── validation_results.json          # Performance on validation
└── validation_summary.json          # Top 10 summary

plots/
├── all_strategies_histogram.png     # Distribution
├── best_vs_validation.png          # Comparison
└── overfitting_proof.png           # Final proof
```

---

## ☁️ AWS Cloud Architecture

### Deployment Option 1: AWS Elastic Beanstalk (Recommended for Simplicity)

**Advantages:**
- Managed platform
- Auto-scaling
- Integrated monitoring
- Easy deployment
- Cost-effective for demo

**Configuration:**
```
Environment: Python 3.11
Platform: Docker
Instance Type: t3.small (or t3.micro for free tier)
Auto Scaling: 1-3 instances
Health Checks: /healthz endpoint
```

### Deployment Option 2: AWS ECS Fargate (Container-First)

**Advantages:**
- Serverless containers
- Better for microservices
- More control
- Industry standard

**Configuration:**
```
Cluster: overfitting-demo-cluster
Service: streamlit-app-service
Task Definition: streamlit-task
    - CPU: 512
    - Memory: 1024 MB
    - Container: streamlit-app:latest
Auto Scaling: Target 70% CPU
```

### Supporting AWS Services

#### Application Load Balancer (ALB)
- HTTPS termination
- Path-based routing
- Health checks
- SSL/TLS certificate (AWS Certificate Manager)

#### Amazon S3
- Static file storage
- Data backup
- Plot image hosting
- Logs archival

#### Amazon CloudWatch
- Application logs
- Metrics (CPU, memory, requests)
- Alarms (high error rates, performance degradation)
- Dashboards

#### AWS IAM
- Service roles
- Least privilege access
- Secrets management

#### Amazon Route 53
- DNS management
- Domain routing
- Health checks

#### AWS Secrets Manager
- API keys (if needed)
- Database credentials
- Configuration secrets

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

**Triggers:**
- Push to `main` branch
- Pull request creation
- Manual trigger

**Pipeline Stages:**

```yaml
1. Code Quality
   ├── Linting (pylint, flake8)
   ├── Type checking (mypy)
   ├── Security scan (bandit)
   └── Dependency check

2. Testing
   ├── Unit tests (pytest)
   ├── Integration tests
   ├── Coverage report (>80%)
   └── Performance tests

3. Build
   ├── Docker image build
   ├── Tag with commit SHA
   ├── Push to AWS ECR
   └── Vulnerability scan

4. Deploy (Staging)
   ├── Deploy to staging environment
   ├── Smoke tests
   ├── Integration tests
   └── Manual approval gate

5. Deploy (Production)
   ├── Blue/Green deployment
   ├── Health checks
   ├── Rollback on failure
   └── Notification (Slack/Email)

6. Post-Deployment
   ├── Monitor CloudWatch
   ├── Verify endpoints
   ├── Update documentation
   └── Create release notes
```

### Deployment Strategy: Blue/Green

**Benefits:**
- Zero downtime
- Easy rollback
- Safe testing
- Gradual traffic shift

**Process:**
```
1. Deploy new version (Green) alongside old version (Blue)
2. Run health checks on Green
3. Shift 10% traffic to Green
4. Monitor metrics
5. Shift 50% traffic to Green
6. Monitor metrics
7. Shift 100% traffic to Green
8. Terminate Blue after 24 hours
```

---

## 🔒 Security Architecture

### Security Layers

#### 1. Network Security
- VPC with private subnets
- Security groups (principle of least privilege)
- NACLs for additional layer
- No public IP for containers (ALB only)

#### 2. Application Security
- HTTPS only (TLS 1.2+)
- CORS configuration
- Rate limiting
- Input validation
- XSS protection

#### 3. Data Security
- S3 bucket encryption (AES-256)
- No sensitive data storage
- Audit logging
- Access logs retention

#### 4. Infrastructure Security
- IAM roles (no hardcoded credentials)
- Secrets Manager for configs
- CloudTrail for audit
- GuardDuty for threat detection

#### 5. Container Security
- Non-root user in Docker
- Minimal base image (python:3.11-slim)
- Regular security scans
- Signed images

---

## 📊 Monitoring & Observability

### CloudWatch Dashboards

**Application Metrics:**
- Request count
- Response time (p50, p95, p99)
- Error rate
- User sessions

**Infrastructure Metrics:**
- CPU utilization
- Memory usage
- Network I/O
- Disk usage

**Business Metrics:**
- Simulations run
- Page views per section
- User engagement time
- Demo completion rate

### Alarms & Alerts

**Critical Alarms:**
- Service down (health check fails)
- Error rate > 5%
- Response time > 3s
- CPU > 80% for 5 minutes

**Warning Alarms:**
- Memory > 70%
- Disk > 80%
- 4xx errors spike
- Unusual traffic patterns

### Logging Strategy

**Log Levels:**
- ERROR: Application failures
- WARNING: Performance degradation
- INFO: User interactions
- DEBUG: Development only

**Log Aggregation:**
- CloudWatch Logs
- Structured JSON format
- Correlation IDs
- Retention: 30 days

---

## 🚀 Scalability & Performance

### Auto-Scaling Configuration

**Metrics-Based Scaling:**
```
Scale Up:
- CPU > 70% for 3 minutes
- Memory > 75% for 3 minutes
- Request count > 1000/min

Scale Down:
- CPU < 30% for 10 minutes
- Memory < 40% for 10 minutes
- Request count < 100/min

Limits:
- Min instances: 1
- Max instances: 5
- Cooldown: 300 seconds
```

### Performance Optimization

**Backend:**
- Streamlit caching (@st.cache_data)
- Lazy loading of data
- Pre-computed results
- Async operations where possible

**Frontend:**
- Plotly for interactive charts (client-side rendering)
- Image optimization
- Lazy loading of components
- Session state management

**Database (if needed):**
- DynamoDB for session storage
- Redis for real-time caching
- Connection pooling
- Query optimization

---

## 💰 Cost Optimization

### Estimated Monthly Cost (AWS)

**Low Traffic (~1000 users/month):**
```
Elastic Beanstalk (t3.small): $15-20
ALB: $20
S3: $1-5
CloudWatch: $5
Route 53: $0.50
Total: ~$40-50/month
```

**Medium Traffic (~10,000 users/month):**
```
ECS Fargate (2 tasks): $30-40
ALB: $25
S3: $5-10
CloudWatch: $10
Route 53: $0.50
Total: ~$70-85/month
```

### Cost Savings Strategies

1. **Use Spot Instances** (for non-critical workloads)
2. **Auto-scaling** (scale down during low traffic)
3. **S3 Lifecycle Policies** (move old data to Glacier)
4. **CloudWatch Log Retention** (reduce to 7 days)
5. **Reserved Instances** (if long-term project)

---

## 🧪 Testing Strategy

### Test Pyramid

```
        ┌─────────────┐
        │    E2E      │  ← 10% (Selenium, Playwright)
        └─────────────┘
       ┌───────────────┐
       │  Integration  │  ← 20% (API tests, Component tests)
       └───────────────┘
      ┌─────────────────┐
      │      Unit       │  ← 70% (pytest, unittest)
      └─────────────────┘
```

### Test Coverage

**Unit Tests:**
- Data loading functions
- Metrics calculations
- Strategy generation
- Statistical functions

**Integration Tests:**
- Full backtest pipeline
- Data persistence
- Chart generation
- API endpoints (if any)

**End-to-End Tests:**
- User workflows
- Page navigation
- Interactive simulations
- Data visualization

**Performance Tests:**
- Load testing (100 concurrent users)
- Stress testing (500 concurrent users)
- Response time benchmarks
- Memory leak detection

---

## 📈 Skills Demonstrated

### Development Skills
- ✅ Python (advanced: pandas, numpy, data science)
- ✅ Web development (Streamlit framework)
- ✅ Data visualization (Plotly, Matplotlib)
- ✅ Software design patterns
- ✅ Clean code practices
- ✅ Git version control

### DevOps Skills
- ✅ Docker containerization
- ✅ CI/CD pipelines (GitHub Actions)
- ✅ Infrastructure as Code
- ✅ Automated testing
- ✅ Monitoring & logging
- ✅ Deployment automation

### Cloud Skills (AWS)
- ✅ ECS / Elastic Beanstalk
- ✅ S3, CloudWatch, IAM
- ✅ Load Balancing (ALB)
- ✅ Auto-scaling
- ✅ Security best practices
- ✅ Cost optimization

### Quantitative Finance Skills
- ✅ Backtesting frameworks
- ✅ Performance metrics (Sharpe, drawdown)
- ✅ Statistical analysis
- ✅ Overfitting detection
- ✅ Walk-forward analysis
- ✅ Risk management concepts

### Data Science Skills
- ✅ Data processing pipelines
- ✅ Statistical modeling
- ✅ Hypothesis testing
- ✅ Data visualization
- ✅ Exploratory analysis
- ✅ Model validation

---

## 🔮 Future Enhancements

### Phase 2 Features
- [ ] Multiple asset classes (stocks, forex, crypto)
- [ ] Real-time data streaming
- [ ] User accounts & saved simulations
- [ ] Comparison with real ML models
- [ ] API for programmatic access

### Phase 3 Features
- [ ] Kubernetes deployment
- [ ] Multi-region deployment
- [ ] A/B testing framework
- [ ] Advanced analytics dashboard
- [ ] Educational video content

### Technology Upgrades
- [ ] React frontend (for more interactivity)
- [ ] FastAPI backend (REST API)
- [ ] PostgreSQL database
- [ ] Redis caching layer
- [ ] Kafka for event streaming

---

## 📝 Documentation Standards

### Code Documentation
- Docstrings for all functions
- Type hints
- README in each module
- Inline comments for complex logic

### API Documentation
- OpenAPI/Swagger spec
- Example requests/responses
- Authentication guide
- Rate limits

### Architecture Documentation
- This document
- Decision records (ADRs)
- Runbooks
- Disaster recovery plan

---

## 🎯 Success Metrics

### Technical Metrics
- **Uptime**: >99.5%
- **Response Time**: <2s (p95)
- **Error Rate**: <1%
- **Deployment Frequency**: Daily
- **Lead Time**: <1 hour
- **MTTR**: <30 minutes

### Business Metrics
- **User Engagement**: >5 min avg session
- **Demo Completion**: >60% reach final page
- **Simulation Runs**: Track interactive usage
- **Recruiter Interest**: Job interview conversions

---

## 📞 Support & Maintenance

### Monitoring
- 24/7 CloudWatch alarms
- Weekly health reports
- Monthly cost reviews
- Quarterly architecture reviews

### Maintenance Windows
- Planned: Sundays 2-4 AM EST
- Emergency: As needed
- Communication: Email/Slack

### Backup & Disaster Recovery
- **Data Backup**: Daily S3 snapshots
- **RTO**: 4 hours
- **RPO**: 24 hours
- **DR Region**: us-west-2

---

## 🏆 Competitive Advantages

This architecture demonstrates:

1. **Production-Ready**: Not just a toy project
2. **Scalable**: Handles growth from 10 to 10,000 users
3. **Secure**: Industry best practices
4. **Cost-Effective**: Optimized for efficiency
5. **Maintainable**: Clean, documented, testable
6. **Modern Stack**: Current technologies
7. **Cloud-Native**: AWS best practices
8. **DevOps Culture**: Automated everything

---

## 📚 References & Resources

- AWS Well-Architected Framework
- Twelve-Factor App Methodology
- Docker Best Practices
- Git Workflow Standards
- Python Style Guide (PEP 8)
- Streamlit Documentation

---

**Version**: 1.0
**Last Updated**: February 2026
**Maintained By**: [Your Name]
**Contact**: [Your Email]
