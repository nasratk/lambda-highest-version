import boto3
import json

lambda_client = boto3.client('lambda')

def get_highest_version(event, context):
    function_name = event['function_name']

    try:
        response = lambda_client.list_versions_by_function(
            FunctionName=function_name,
            MaxItems=100 
        )

        versions = response['Versions']

        # Filter and find max numeric version (changed to list comprehension)
        numbered_versions = [int(v['Version']) for v in versions if v['Version'] != '$LATEST']

        if numbered_versions:
            highest_version = max(numbered_versions)
        else:
            highest_version = 0  # Return 0 if no numbered versions found

        return {
            'statusCode': 200,
            'body': json.dumps({'highest_version': highest_version})
        }

    except lambda_client.exceptions.ResourceNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Lambda function not found'})
        }
