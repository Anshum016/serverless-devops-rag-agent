resource "aws_s3_bucket" "knowledge_base" {
  bucket = "log-rag-agent-storage-${data.aws_caller_identity.current.account_id}"
  force_destroy = true
}

# Trigger Configuration ---

# Permission: Allow S3 to call the Ingest Lambda
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingest_worker.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.knowledge_base.arn
}

#Notification: Tell S3 to actually send the event
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.knowledge_base.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.ingest_worker.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "raw/"  # Only trigger for files in the 'raw' folder
  }

  depends_on = [aws_lambda_permission.allow_s3]
}

# Output the bucket name
output "s3_bucket_name" {
  value = aws_s3_bucket.knowledge_base.id
}