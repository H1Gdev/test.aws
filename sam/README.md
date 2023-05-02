# [AWS Serverless Application Model(SAM)](https://aws.amazon.com/serverless/sam)

- [Documentation](https://docs.aws.amazon.com/serverless-application-model/)

## AWS SAM template specification

- [AWS SAM transform](https://github.com/aws/serverless-application-model)
  - `AWS CloudFormation macro` that transforms `AWS SAM Templates` into `AWS CloudFormation Templates`.

## AWS SAM Command Line Interface(CLI)

- [Install AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
  - [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [AWS SAM CLI Application Templates](https://github.com/aws/aws-sam-cli-app-templates)
- [Lambda Builders](https://github.com/aws/aws-lambda-builders/)

### Create an App

```shell
sam init

Which template source would you like to use?
	1 - AWS Quick Start Templates
Choice: 1

Choose an AWS Quick Start application template
	1 - Hello World Example
Template: 1

Use the most popular runtime and package type? (Python and zip) [y/N]: N

Which runtime would you like to use?
	13 - nodejs18.x
Runtime: 13

What package type would you like to use?
	1 - Zip
Package type: 1

Based on your selections, the only dependency manager available is npm.
We will proceed copying the template using npm.

Select your starter template
	1 - Hello World Example
Template: 1

Would you like to enable X-Ray tracing on the function(s) in your application?  [y/N]: N

Would you like to enable monitoring using CloudWatch Application Insights?
For more info, please view https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-application-insights.html [y/N]: N

Project name [sam-app]: sam-app
```

### Develop your App

```shell
cd sam-app
sam build

# Specify resource
sam build <RESOURCE_LOGICAL_ID>
```

### Deploy your App

```shell
sam deploy --guided

# Continuous
sam deploy
```

```shell
sam package
```

### And More

```shell
sam delete
```

For permanently delete, also do the following:

1. Delete `aws-sam-cli-managed-default-samclisourcebucket-XXXX` from `Amazon S3` `Buckets`.
2. Delete `aws-sam-cli-managed-default` from `AWS CloudFormation` `Stacks`.

### Options

```shell
sam --version

SAM CLI, version 1.81.0
```

