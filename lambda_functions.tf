
# GETTING TWEETS LAMBDA FUNCTION
resource aws_lambda_function gettingtweets {

  function_name = "gettingtweets-${var.environment}"
  role = var.lambda_role
  timeout = var.timeout
  memory_size = 128
  image_uri = "${var.base_image_uri}gettingtweets"
  package_type = "Image"

  environment {
    variables = {
      S3_BUCKET_NAME=var.bucket_name
      S3_LANDING_LAYER="bronze"
      BEARER_TOKEN=var.BEARER_TOKEN
  }
 }
}
 

# PROCESSING RAW LAMBDA FUNCTION
resource aws_lambda_function processingraw {

  function_name = "processingraw-${var.environment}"
  role = var.lambda_role
  timeout = var.timeout
  memory_size = 1024
  image_uri = "${var.base_image_uri}processingraw"
  package_type = "Image"

  environment {
    variables = {
      S3_BUCKET_NAME=var.bucket_name
    }
  }
}


# TWEETS TO SILVER LAMBDA FUNCTION
resource aws_lambda_function tweetstosilver {

  function_name = "tweetstosilver-${var.environment}"
  role = var.lambda_role
  timeout = var.timeout
  memory_size = 2048
  image_uri = "${var.base_image_uri}tweetstosilver"
  package_type = "Image"

  environment {
    variables = {
      S3_BUCKET_NAME=var.bucket_name
    }
  }
}


# USERS TO SILVER LAMBDA FUNCTION
resource aws_lambda_function userstosilver {

  function_name = "userstosilver-${var.environment}"
  role = var.lambda_role
  timeout = var.timeout
  memory_size = 1024
  image_uri = "${var.base_image_uri}userstosilver"
  package_type = "Image"

    environment {
    variables = {
      S3_BUCKET_NAME=var.bucket_name
    }
  }
}


# PLACES TO SILVER LAMBDA FUNCTION
resource aws_lambda_function placestosilver {

  function_name = "placestosilver-${var.environment}"
  role = var.lambda_role
  timeout = var.timeout
  memory_size = 1024
  image_uri = "${var.base_image_uri}placestosilver"
  package_type = "Image"

  environment {
    variables = {
      S3_BUCKET_NAME=var.bucket_name
    }
  }
}




output "gettingtweets_name" {
 value = aws_lambda_function.gettingtweets.arn
}

output "processingraw_name" {
 value = aws_lambda_function.processingraw.arn
}

output "tweetstosilver_name" {
 value = aws_lambda_function.tweetstosilver.arn
}

output "userstosilver_name" {
 value = aws_lambda_function.userstosilver.arn
}

output "placestosilver_name" {
 value = aws_lambda_function.placestosilver.arn
}