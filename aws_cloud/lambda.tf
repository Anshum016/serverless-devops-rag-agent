#THE CHAT AGENT (Reads from S3) 
resource "aws_lambda_function" "rag_agent" {
  function_name = "log-rag-agent-function"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.repo.repository_url}:latest"
  
  timeout       = 30
  memory_size   = 1024
  architectures = ["x86_64"]

  environment {
    variables = {
      GOOGLE_API_KEY = var.google_api_key
      BUCKET_NAME    = aws_s3_bucket.knowledge_base.id 
    }
  }

  depends_on = [docker_registry_image.push]
}

#THE INGEST WORKER (Writes to S3) 
resource "aws_lambda_function" "ingest_worker" {
  function_name = "log-rag-ingest-worker"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.repo.repository_url}:latest"

  # OVERRIDE COMMAND: Run ingest.py instead of the default
  image_config {
    command = ["ingest.lambda_handler"]
  }

  timeout       = 300 
  memory_size   = 1024
  architectures = ["x86_64"]

  environment {
    variables = {
      GOOGLE_API_KEY = var.google_api_key
      BUCKET_NAME    = aws_s3_bucket.knowledge_base.id
    }
  }

  depends_on = [docker_registry_image.push]
}