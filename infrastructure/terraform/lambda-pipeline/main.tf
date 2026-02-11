terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "OverfittingDemo"
      ManagedBy   = "Terraform"
      Environment = var.environment
      Component   = "Lambda-Pipeline"
    }
  }
}

# Variables
variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  default     = "production"
}

variable "app_name" {
  description = "Application name"
  default     = "overfitting-demo"
}

# Data sources to reference main infrastructure
data "aws_s3_bucket" "data" {
  bucket = "${var.app_name}-data"
}
