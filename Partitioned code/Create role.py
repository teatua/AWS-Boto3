# Import necessary libraries
import boto3
import json

# Specify the SSO profile name that you want to use
sso_profile_name = "boto3"

# Create a Boto3 session using the SSO profile
session = boto3.Session(profile_name=sso_profile_name)

# Create an IAM client using the custom SSO profile
iam = session.client('iam')

# Pick a name for this role
role_name = 'Ninja'
# The assume role policy specifies that only the Security Token Service (STS) can assume the role, and that the STS user must have MFA enabled.
assume_role_policy = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
        "Principal": {
        "Service": "sts.amazonaws.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "Bool": {
          "aws:MultiFactorAuthPresent": "true"
        }
      }
    }
  ]
}

iam.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=json.dumps(assume_role_policy) #AssumeRolePolicyDocument must be a JSON string.
)
# Print confirmation on console
print('Role created:', role_name)