terraform {
  backend "s3" {
    bucket = "convo-ai-tfstate" # TODO: Set actual bucket
    key    = "state/infra.tfstate" # TODO: Set actual key
    region = "ap-south-1"
  }
} 