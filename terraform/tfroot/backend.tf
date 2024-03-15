# terraform {
#   required_version = "~> 1.5.0"
#   backend "s3" {
#     bucket = "[tfstateを格納するバケット]"
#     region = "ap-northeast-1"
#     key    = "key/terraform.tfstate"
#   }
# }

# resource "aws_s3_bucket" "dwh_terraform_state" {
#   bucket = "[tfstateを格納するバケット]"
# }

# resource "aws_s3_bucket_versioning" "versioning" {
#   bucket = aws_s3_bucket.dwh_terraform_state.id
#   versioning_configuration {
#     status = "Enabled"
#   }
# }