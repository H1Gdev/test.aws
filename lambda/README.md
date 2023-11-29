# [AWS Lambda](https://aws.amazon.com/lambda/)

- [Documentation](https://docs.aws.amazon.com/lambda/)

## Powertools for AWS Lambda

- [Powertools for AWS Lambda (Python)](https://awslabs.github.io/aws-lambda-powertools-python/)
- [Powertools for AWS Lambda (Java)](https://awslabs.github.io/aws-lambda-powertools-java/)
- [Powertools for AWS Lambda (TypeScript)](https://awslabs.github.io/aws-lambda-powertools-typescript/)
- [Powertools for AWS Lambda (.NET)](https://awslabs.github.io/aws-lambda-powertools-dotnet/)

### Features

- Core utilities
  - [Tracer](#tracer)
  - [Logger](#logger)
  - Metrics
  - Event Handler
    - REST API
    - GraphQL API
- Utilities
  - Parameters
  - Batch Processing
  - Typing
  - Validation
  - Event Source Data Classes
  - Parser (Pydantic)
  - Idempotency
  - Feature flags
  - Streaming
  - Middleware factory
  - JMESPath Functions
  - CloudFormation Custom Resources
  - Idempotency
  - SQS Large Message Handling
  - SQS Batch Processing
  - Custom Resources
  - Serialization Utilities

#### Tracer

`AWS X-Ray SDK` wrapper.

#### Logger

##### log level

Set `Log Level` > Constructor > Environment variable(`LOG_LEVEL` or `POWERTOOLS_LOG_LEVEL`) > (`log4j2`) > Default
