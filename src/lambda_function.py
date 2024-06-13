import boto3
import json

lambda_client = boto3.client('lambda')

def get_highest_version(event, context):
    function_name = event['function_name']

    try:
        response = lambda_client.list_versions_by_function(
            FunctionName=function_name,
            MaxItems=100  # Adjust if you have many versions
        )

        versions = response['Versions']

        # Filter out $LATEST and find the max numeric version
        highest_version = max(
            (int(v['Version']) for v in versions if v['Version'] != '$LATEST'),
            default=None
        )

        if highest_version:
            return {
                'statusCode': 200,
                'body': json.dumps({'highest_version': highest_version})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No published versions found'})
            }

    except lambda_client.exceptions.ResourceNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Lambda function not found'})
        }