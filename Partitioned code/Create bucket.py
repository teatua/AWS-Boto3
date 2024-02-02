# Import necessary libraries
import boto3

# Specify the SSO profile name that you want to use
sso_profile_name = "boto3"

# Create a Boto3 session using the SSO profile
session = boto3.Session(profile_name=sso_profile_name)

# Create a S3 client
s3 = session.client('s3')

# Create an S3 bucket to store the configuration
bucket_name = 'config-easyas123-popo'  # Specify your desired bucket name (Must be unique globally, no other AWS accounts in the world must have used it)
s3.create_bucket(Bucket=bucket_name)

print(f"Created S3 bucket: {bucket_name}") #Print confirmation on console