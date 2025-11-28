resource "aws_iam_role" "lambda_role" {
  name = "log_agent_lambda_role_v2"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

#S3 PERMISSIONS 
resource "aws_iam_policy" "s3_access" {
  name        = "log_agent_s3_policy"
  description = "Allow reading and writing to the Knowledge Base bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",    # For Agent (Download)
          "s3:PutObject",    # For Ingest Worker (Upload)
          "s3:ListBucket"
        ]
        Resource = [
          "${aws_s3_bucket.knowledge_base.arn}",
          "${aws_s3_bucket.knowledge_base.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_s3" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_access.arn
}