# Import necessary libraries
import boto3
import json

# Initialise session
session = boto3.Session(profile_name='boto3')
# Create a S3 & IAM client
s3 = session.client('s3')

# Specify the S3 bucket name and key
s3_bucket_name = 'your-s3-bucket-name'                     ###Chose your s3 bucket name key####
s3_key = 'iam-configuration.json'                          ####Chose your s3 key####

# Define the IAM configuration to store in S3
config = {
    'Users': users,                                       #### PUT IN THE USERS NAMES OR VALUABLE ####
    'Role': role_name,                                    #### PUT IN THE ROLE NAMES / VALUABLE ####
    'Policies': [policy_name1, policy_name2]              #### PUT IN THE POLICY NAMES / VALUABLE ####
}

# Put the IAM configuration in the specified S3 bucket
s3.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=json.dumps(config))

# Print a confirmation message
print(f"IAM configuration stored in S3 bucket: {s3_bucket_name}/{s3_key}")