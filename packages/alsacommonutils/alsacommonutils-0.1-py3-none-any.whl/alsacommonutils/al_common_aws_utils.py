import boto3
import traceback
from botocore.exceptions import ClientError

## Utility Functions ###
def get_secret(secret_name, region_name):
    # Pass the required AWS Region in which Secret is stored

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response["SecretString"]
    return secret

def get_parameter(param_name,WithDecryption=True):
    """Retrieves parameter from AWS Parameter Store
    Args:
        'param_name' (str): name of parameter
    """
    try:
        ssm = boto3.client("ssm", region_name="eu-west-1")
        parameter = ssm.get_parameter(Name=param_name, WithDecryption=WithDecryption)
        return parameter["Parameter"]["Value"]
    except ClientError as e:
        error_msg = "Failed to get value for ssm parameter '" + param_name + "'"
        print("Error occured: " + error_msg + " - " + str(e))
        print(traceback.format_exc())        
        raise e
        #raise ClientError(error_msg) from e
