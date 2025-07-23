output "recordings_bucket" {
  value = aws_s3_bucket.call_recordings.bucket
}

output "twilio_phone_number" {
  value = "+17727327388"
  description = "Twilio number for inbound calls (set webhook in console)"
}

# TODO: Output Twilio phone number when resource is added 