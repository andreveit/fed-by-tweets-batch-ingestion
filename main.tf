terraform {
  # backend "remote" {
  cloud {
    organization = "fedbytweets-batchingestion"
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = var.aws_region
}


resource "aws_cloudwatch_event_rule" "batch-workflow-rule" {
  name                = "batch-workflow-${var.environment}"
  description         = "Ingestion Pipeline"
  schedule_expression = "cron(59 9/7 * * ? *)" # Running at 7, 14 and 21h Brazillian Time
}

resource "aws_cloudwatch_event_target" "batch-workflow-target" {
  target_id = "RunPipeline"
  arn       = aws_sfn_state_machine.ingestion-workflow.arn
  rule      = aws_cloudwatch_event_rule.batch-workflow-rule.name
  role_arn  = var.event_target_role
  input     =jsonencode(
    {
      "start": "True"
    }
    )

depends_on = [
    aws_sfn_state_machine.ingestion-workflow
  ]
}
