variable "aws_region" {
  description = "AWS region for resources"
  default     = "ap-south-1"
}

variable "twilio_auth_token" {
  description = "Twilio Auth Token"
  type        = string
  sensitive   = true
  # TODO: Set via environment or secrets manager
}

variable "twilio_account_sid" {
  description = "Twilio Account SID"
  type        = string
  sensitive   = true
}

variable "recordings_bucket_name" {
  description = "S3 bucket for call recordings"
  default     = "convo-ai-call-recordings"
} 