
resource "aws_sfn_state_machine" "ingestion-workflow" {
  name     = "ingestion-workflow-${var.environment}"
  role_arn = "${var.step_function_role}"
  depends_on = [
    aws_lambda_function.gettingtweets,
    aws_lambda_function.processingraw,
    aws_lambda_function.tweetstosilver,
    aws_lambda_function.userstosilver,
    aws_lambda_function.placestosilver,
  ]
  
  definition = <<EOF

{
    "Comment": "Tweets ingestion workflow",
    "StartAt": "get-tweets",
    "States": {
      "get-tweets": {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "OutputPath": "$.Payload",
        "Parameters": {
          "Payload.$": "$",
          "FunctionName": "${aws_lambda_function.gettingtweets.arn}:$LATEST"
        },
        "Retry": [
          {
            "ErrorEquals": [
              "Lambda.ServiceException",
              "Lambda.AWSLambdaException",
              "Lambda.SdkClientException"
            ],
            "IntervalSeconds": 2,
            "MaxAttempts": 6,
            "BackoffRate": 2
          }
        ],
        "Next": "processing-raw"
      },
      "processing-raw": {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "OutputPath": "$.Payload",
        "Parameters": {
          "Payload.$": "$",
          "FunctionName": "${aws_lambda_function.processingraw.arn}:$LATEST"
        },
        "Retry": [
          {
            "ErrorEquals": [
              "Lambda.ServiceException",
              "Lambda.AWSLambdaException",
              "Lambda.SdkClientException"
            ],
            "IntervalSeconds": 2,
            "MaxAttempts": 6,
            "BackoffRate": 2
          }
        ],
        "Next": "Parallel"
      },
      "Parallel": {
        "Type": "Parallel",
        "Branches": [
          {
            "StartAt": "tweets-to-silver",
            "States": {
              "tweets-to-silver": {
                "Type": "Task",
                "Resource": "arn:aws:states:::lambda:invoke",
                "OutputPath": "$.Payload",
                "Parameters": {
                  "Payload.$": "$",
                  "FunctionName": "${aws_lambda_function.tweetstosilver.arn}:$LATEST"
                },
                "Retry": [
                  {
                    "ErrorEquals": [
                      "Lambda.ServiceException",
                      "Lambda.AWSLambdaException",
                      "Lambda.SdkClientException"
                    ],
                    "IntervalSeconds": 2,
                    "MaxAttempts": 6,
                    "BackoffRate": 2
                  }
                ],
                "End": true
              }
            }
          },
          {
            "StartAt": "users-to-silver",
            "States": {
              "users-to-silver": {
                "Type": "Task",
                "Resource": "arn:aws:states:::lambda:invoke",
                "OutputPath": "$.Payload",
                "Parameters": {
                  "Payload.$": "$",
                  "FunctionName": "${aws_lambda_function.userstosilver.arn}:$LATEST"
                },
                "Retry": [
                  {
                    "ErrorEquals": [
                      "Lambda.ServiceException",
                      "Lambda.AWSLambdaException",
                      "Lambda.SdkClientException"
                    ],
                    "IntervalSeconds": 2,
                    "MaxAttempts": 6,
                    "BackoffRate": 2
                  }
                ],
                "End": true
              }
            }
          },
          {
            "StartAt": "places-to-silver",
            "States": {
              "places-to-silver": {
                "Type": "Task",
                "Resource": "arn:aws:states:::lambda:invoke",
                "OutputPath": "$.Payload",
                "Parameters": {
                  "Payload.$": "$",
                  "FunctionName": "${aws_lambda_function.placestosilver.arn}:$LATEST"
                },
                "Retry": [
                  {
                    "ErrorEquals": [
                      "Lambda.ServiceException",
                      "Lambda.AWSLambdaException",
                      "Lambda.SdkClientException"
                    ],
                    "IntervalSeconds": 2,
                    "MaxAttempts": 6,
                    "BackoffRate": 2
                  }
                ],
                "End": true
              }
            }
          }
        ],
        "End": true
      }
    }
  }

  EOF

}


output "ingestion-workflow" {value = "${aws_sfn_state_machine.ingestion-workflow.arn}"}