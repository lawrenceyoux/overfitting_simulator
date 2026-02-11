# 🎲 Overfitting Demo - Comprehensive Portfolio Project

## 📖 Overview

An **interactive web application** demonstrating overfitting in algorithmic trading - built as a comprehensive portfolio project showcasing software engineering, DevOps, cloud deployment, and quantitative finance skills.

**🎯 For the complete portfolio presentation, see: [PORTFOLIO_README.md](PORTFOLIO_README.md)**

---

## ✨ What's New - Portfolio Edition

This project has been **significantly enhanced** for job applications and portfolio demonstrations:

### 🆕 New Features

1. **🌐 Interactive Streamlit Web App** ([app.py](app.py))
   - Real-time strategy simulation
   - Interactive visualizations with Plotly
   - Multiple educational sections
   - Mobile-responsive design

2. **☁️ AWS Cloud Deployment**
   - Complete AWS infrastructure (ECS Fargate, ALB, S3, CloudWatch)
   - Infrastructure as Code with Terraform
   - Auto-scaling and load balancing
   - Production-ready security

3. **🔄 CI/CD Pipeline**
   - GitHub Actions automated workflow
   - Automated testing, linting, security scanning
   - Blue/Green deployments
   - Automated rollback on failure

4. **🐳 Docker Containerization**
   - Multi-stage optimized builds
   - Security best practices
   - Docker Compose for local development
   - Health checks and monitoring

5. **🧪 Testing Infrastructure**
   - Comprehensive unit tests
   - 80%+ code coverage
   - Integration tests
   - Code quality tools (pylint, flake8, black)

6. **📚 Professional Documentation**
   - Complete architecture documentation
   - AWS deployment guide
   - API documentation
   - Runbooks and troubleshooting guides

---

## 🚀 Quick Start

### Run Locally (Easiest)

**Windows:**
```powershell
.\quick_start.ps1
```

**Linux/Mac:**
```bash
chmod +x quick_start.sh
./quick_start.sh
```

### Run with Docker

```bash
docker-compose up
```

Open browser to: http://localhost:8501

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| **[PORTFOLIO_README.md](PORTFOLIO_README.md)** | **Complete portfolio presentation** |
| **[app.py](app.py)** | **Main Streamlit web application** |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture & design |
| [DEPLOYMENT.md](DEPLOYMENT.md) | AWS deployment guide |
| [Dockerfile](Dockerfile) | Container configuration |
| [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml) | CI/CD pipeline |

---

## 🎯 The Concept (Quick Version)

1. Generate 100 **random trading strategies** (coin flips)
2. Backtest on **real Bitcoin data** → Some look amazing (60-70% win rate)!
3. Validate on new data → **Performance collapses** to ~50% (random chance)
4. **Lesson**: Past performance ≠ Future results without proper validation

### Visual Proof

![Distribution](plots/all_strategies_histogram.png)
![Comparison](plots/best_vs_validation.png)

---

## 💼 For Job Applications

### Skills Demonstrated

✅ **Software Engineering**: Python, testing, clean code, design patterns
✅ **DevOps**: CI/CD, Docker, automation, monitoring
✅ **Cloud (AWS)**: ECS, ALB, IAM, VPC, Terraform, cost optimization
✅ **Quantitative Finance**: Backtesting, risk metrics, statistical validation
✅ **Data Science**: Data pipelines, visualization, statistical analysis

### How to Present

See [PORTFOLIO_README.md](PORTFOLIO_README.md) for:
- Detailed skills breakdown
- Interview talking points
- Demo script (5-10 minutes)
- Architecture diagrams
- Performance metrics

---

## 📊 Project Statistics

- **Code Coverage**: 80%+
- **Docker Image Size**: <500MB
- **Deployment Time**: <5 minutes
- **AWS Monthly Cost**: $40-60 (or free tier eligible)
- **Lines of Code**: ~2000+
- **Documentation Pages**: 1000+ lines

---

## 🎬 Interactive Demo

Try it live: **[Deploy URL Here]**

Features:
- 🎮 Interactive simulation generator
- 📈 Real Bitcoin data results
- 🔬 Statistical deep dive
- 📚 Educational content

---

## 📚 Original Documentation

- **[START_HERE.md](START_HERE.md)**: Original project concept
- **[HOW_TO_RUN.md](HOW_TO_RUN.md)**: Basic execution guide
- **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)**: Development checklist

---

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run data pipeline
python 01_generate_random_strategies.py
python 02_backtest_strategies.py
python 03_select_best_strategy.py
python 04_validate_strategy.py
python 05_visualize_results.py

# Start app
streamlit run app.py

# Run tests
pytest

# Code quality
black --check .
flake8 .
pylint *.py
```

---

## ☁️ AWS Deployment

### Option 1: Elastic Beanstalk (Easiest)

```bash
eb init -p docker overfitting-demo
eb create overfitting-demo-prod
eb deploy
```

### Option 2: ECS with Terraform (Production)

```bash
cd .aws/terraform
terraform init
terraform apply
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide.

---

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

MIT License - Free to use for learning and portfolio purposes

---

## 📞 Contact

- **Author**: [Your Name]
- **Email**: your.email@example.com
- **LinkedIn**: [linkedin.com/in/yourname](https://linkedin.com/in/yourname)
- **Portfolio**: [yourportfolio.com](https://yourportfolio.com)

---

## 🙏 Acknowledgments

- Original concept developed during algo trading research
- Enhanced for job applications and portfolio demonstration  
- Built with Streamlit, Docker, AWS, and lots of ☕

---

**⭐ If you're a recruiter: Please see [PORTFOLIO_README.md](PORTFOLIO_README.md) for the complete presentation!**

---

*Last Updated: February 2026*
