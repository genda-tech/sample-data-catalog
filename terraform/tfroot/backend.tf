terraform {
  required_version = "~> 1.5.0"
  backend "s3" {
    bucket = "${var.bucket}"
    region = "${var.region}"
    key    = "key/terraform.tfstate"
  }
}

resource "aws_s3_bucket" "dwh_terraform_state" {
  bucket = "${var.bucket}"
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.dwh_terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}