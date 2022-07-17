variable "BEARER_TOKEN" {
  type     = string
  sensitive = true
  nullable = false
}


variable "aws_region" {
  default = "us-east-1"
}


variable "timeout" {
  default = 900
}




variable "lambda_role" {
    description = "Role to be assigned to the Lambda Functions"
}


variable "step_function_role" {
    description = "Role to be assigned to the Step Function"
}


variable "event_target_role" {
    description = "Role to be assigned to the Invoker"
}




variable "environment" {
    description = "staging or production"
}

variable "bucket_name" {
    description = "Setup according to the environment"
    # default = "twitter-project-data-lake-andre-staging"
}


variable "base_image_uri" {
    description = "Setup according to the environment"
    # default = "356582812311.dkr.ecr.us-east-1.amazonaws.com/ingestion-staging:"
}




