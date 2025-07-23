# Terraform config for infra
provider "aws" {
  region = "ap-south-1"
}

# TODO: Twilio provider setup
provider "twilio" {
  account_sid = var.twilio_account_sid
  auth_token  = var.twilio_auth_token
}

# S3 bucket for call recordings
resource "aws_s3_bucket" "call_recordings" {
  bucket = "convo-ai-call-recordings"
  force_destroy = true
  lifecycle {
    prevent_destroy = false
  }
  # TODO: Add SSE-KMS encryption
  # TODO: Add 90-day lifecycle rule
}

# TODO: Twilio phone number resource
# resource "twilio_phone_number" "main" {}

# NOTE: Phone number (772) 732-7388 is managed manually in Twilio Console.
# To manage via Terraform, import the number or create a resource like below:
# resource "twilio_incoming_phone_number" "main" {
#   phone_number = "+17727327388"
#   voice_url    = "https://<your-domain-or-ngrok>/ws/twilio"
#   voice_method = "POST"
# }

output "recordings_bucket" {
  value = aws_s3_bucket.call_recordings.bucket
} 