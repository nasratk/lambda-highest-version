# LambdaVersionFinder

This AWS Lambda function, named `LambdaVersionFinder`, is designed to query AWS Lambda functions and return the highest published version of a specified Lambda function. The infrastructure is defined using AWS SAM (Serverless Application Model) and is deployed within a specified VPC and subnets.

## Context

This is a very simple Lambda function can be deployed directly as a stand-alone Lambda function. But it's primary purpose is to serve as an example to deploying a CICD pipeline which is set out in the repository **deploy-lambda-from-repo-cicd**.

## Files

- `src/lambda_function.py`: Contains the Lambda function code.
- `template.yaml`: AWS SAM template for defining the Lambda function and its associated resources.
- `buildspec.yaml`: This is used only if this code is used as part of CICD pipeline. It contains the build specs for CodeBuild project. This needs to be copied over from the repository `deploy-lambda-from-repo-cicd`.

## SAM Template

The `template.yaml` defines the following resources:

- **LambdaVersionFinderFunction**: The Lambda function that queries for the highest version.
- **LambdaExecutionRole**: IAM role for the Lambda function with necessary permissions.
- **LambdaVersionFinderSecurityGroup**: Security group for the Lambda function.
- **LiveAlias**: Alias for the Lambda function pointing to `$LATEST`.

### Parameters

- **FunctionName**: Name of the Lambda function (default: `LambdaVersionFinder`).
- **VpcId**: ID of the VPC.
- **SubnetId1**: ID of the first subnet.
- **SubnetId2**: ID of the second subnet.

## Deployment

If you want to deploy this code manually; i.e. without setting up a CICD pipeline, follow the steps below:

1. **Package the application:**

    ```bash
    sam package --output-template-file packaged.yaml --s3-bucket <your-s3-bucket-name>
    ```

2. **Deploy the application:**

    ```bash
    sam deploy --template-file packaged.yaml --stack-name <your-stack-name> --capabilities CAPABILITY_IAM
    ```

3. **Monitor the deployment:**

    You can monitor the deployment process in the AWS CloudFormation console.

## Usage

To invoke the Lambda function, you can use the AWS Lambda console or the AWS CLI. Here’s an example using AWS CLI:

```bash
aws lambda invoke \
    --function-name LambdaVersionFinder \
    --payload '{"function_name": "your-lambda-function-name"}' \
    response.json