# ==============================================
# Lambda Functions for Data Pipeline
# ==============================================

# IAM Role for Lambda Functions
resource "aws_iam_role" "lambda_execution" {
  name = "${var.app_name}-lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.app_name}-lambda-role"
  }
}

# Attach basic Lambda execution policy
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Custom policy for S3 access
resource "aws_iam_role_policy" "lambda_s3_access" {
  name = "${var.app_name}-lambda-s3-policy"
  role = aws_iam_role.lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          data.aws_s3_bucket.data.arn,
          "${data.aws_s3_bucket.data.arn}/*"
        ]
      }
    ]
  })
}

# Lambda Function 1: Generate Strategies
resource "aws_lambda_function" "generate_strategies" {
  function_name = "${var.app_name}-generate-strategies"
  role          = aws_iam_role.lambda_execution.arn
  handler       = "01_generate_strategies_lambda.lambda_handler"
  runtime       = "python3.11"
  timeout       = 300 # 5 minutes
  memory_size   = 512

  filename         = "${path.module}/../../lambda/lambda_package.zip"
  source_code_hash = filebase64sha256("${path.module}/../../lambda/lambda_package.zip")

  environment {
    variables = {
      S3_BUCKET = data.aws_s3_bucket.data.id
    }
  }

  tags = {
    Name = "${var.app_name}-generate-strategies"
  }
}

# Lambda Function 2: Backtest Strategies
resource "aws_lambda_function" "backtest_strategies" {
  function_name = "${var.app_name}-backtest-strategies"
  role          = aws_iam_role.lambda_execution.arn
  handler       = "02_backtest_strategies_lambda.lambda_handler"
  runtime       = "python3.11"
  timeout       = 600 # 10 minutes (backtesting can take time)
  memory_size   = 1024

  filename         = "${path.module}/../../lambda/lambda_package.zip"
  source_code_hash = filebase64sha256("${path.module}/../../lambda/lambda_package.zip")

  environment {
    variables = {
      S3_BUCKET = data.aws_s3_bucket.data.id
    }
  }

  tags = {
    Name = "${var.app_name}-backtest-strategies"
  }
}

# Lambda Function 3: Select Best Strategy
resource "aws_lambda_function" "select_best" {
  function_name = "${var.app_name}-select-best"
  role          = aws_iam_role.lambda_execution.arn
  handler       = "03_select_best_lambda.lambda_handler"
  runtime       = "python3.11"
  timeout       = 180
  memory_size   = 512

  filename         = "${path.module}/../../lambda/lambda_package.zip"
  source_code_hash = filebase64sha256("${path.module}/../../lambda/lambda_package.zip")

  environment {
    variables = {
      S3_BUCKET = data.aws_s3_bucket.data.id
    }
  }

  tags = {
    Name = "${var.app_name}-select-best"
  }
}

# Lambda Function 4: Validate Strategy
resource "aws_lambda_function" "validate_strategy" {
  function_name = "${var.app_name}-validate-strategy"
  role          = aws_iam_role.lambda_execution.arn
  handler       = "04_validate_strategy_lambda.lambda_handler"
  runtime       = "python3.11"
  timeout       = 300
  memory_size   = 512

  filename         = "${path.module}/../../lambda/lambda_package.zip"
  source_code_hash = filebase64sha256("${path.module}/../../lambda/lambda_package.zip")

  environment {
    variables = {
      S3_BUCKET = data.aws_s3_bucket.data.id
    }
  }

  tags = {
    Name = "${var.app_name}-validate-strategy"
  }
}

# Lambda Function 5: Generate Visualizations
resource "aws_lambda_function" "visualize" {
  function_name = "${var.app_name}-visualize"
  role          = aws_iam_role.lambda_execution.arn
  handler       = "05_visualize_lambda.lambda_handler"
  runtime       = "python3.11"
  timeout       = 300
  memory_size   = 1024 # More memory for matplotlib

  filename         = "${path.module}/../../lambda/lambda_package.zip"
  source_code_hash = filebase64sha256("${path.module}/../../lambda/lambda_package.zip")

  environment {
    variables = {
      S3_BUCKET = data.aws_s3_bucket.data.id
    }
  }

  tags = {
    Name = "${var.app_name}-visualize"
  }
}

# ==============================================
# Step Functions State Machine
# ==============================================

# IAM Role for Step Functions
resource "aws_iam_role" "step_functions" {
  name = "${var.app_name}-step-functions-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.app_name}-step-functions-role"
  }
}

# Policy for Step Functions to invoke Lambda
resource "aws_iam_role_policy" "step_functions_lambda" {
  name = "${var.app_name}-step-functions-policy"
  role = aws_iam_role.step_functions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = [
          aws_lambda_function.generate_strategies.arn,
          aws_lambda_function.backtest_strategies.arn,
          aws_lambda_function.select_best.arn,
          aws_lambda_function.validate_strategy.arn,
          aws_lambda_function.visualize.arn
        ]
      }
    ]
  })
}

# Read the state machine definition and substitute variables
locals {
  state_machine_definition = templatefile("${path.module}/../aws/step-functions-state-machine.json", {
    GenerateStrategiesLambdaArn = aws_lambda_function.generate_strategies.arn,
    BacktestStrategiesLambdaArn = aws_lambda_function.backtest_strategies.arn,
    SelectBestStrategyLambdaArn = aws_lambda_function.select_best.arn,
    ValidateStrategyLambdaArn   = aws_lambda_function.validate_strategy.arn,
    VisualizeLambdaArn          = aws_lambda_function.visualize.arn,
    S3BucketName                = data.aws_s3_bucket.data.id
  })
}

# Step Functions State Machine
resource "aws_sfn_state_machine" "data_pipeline" {
  name     = "${var.app_name}-data-pipeline"
  role_arn = aws_iam_role.step_functions.arn

  definition = local.state_machine_definition

  tags = {
    Name = "${var.app_name}-data-pipeline"
  }
}

# ==============================================
# Outputs
# ==============================================

output "step_functions_arn" {
  description = "ARN of the Step Functions state machine"
  value       = aws_sfn_state_machine.data_pipeline.arn
}

output "s3_bucket_name" {
  description = "Name of the S3 data bucket"
  value       = data.aws_s3_bucket.data.id
}

output "lambda_functions" {
  description = "Map of Lambda function names and ARNs"
  value = {
    generate_strategies = aws_lambda_function.generate_strategies.arn
    backtest_strategies = aws_lambda_function.backtest_strategies.arn
    select_best         = aws_lambda_function.select_best.arn
    validate_strategy   = aws_lambda_function.validate_strategy.arn
    visualize           = aws_lambda_function.visualize.arn
  }
}
