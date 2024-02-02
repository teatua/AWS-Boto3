# Import libraries
import boto3
import json

# Specify the SSO profile name that you want to use
sso_profile_name = "boto3"

# Create a Boto3 session using the SSO profile
session = boto3.Session(profile_name=sso_profile_name)

# Create an IAM & s3 client 
iam = session.client('iam')
s3 = session.client('s3')

#=================================================================================================================================================================

# Create an S3 bucket to store the configuration
bucket_name = 'config-easyas123-popo'  # Specify your desired bucket name (Must be unique globally, no other AWS accounts in the world must have used it)
s3.create_bucket(Bucket=bucket_name)

print(f"Created S3 bucket: {bucket_name}") 

#=================================================================================================================================================================

# Create IAM Users 
users = ['User11', 'User21', 'User31']
created_users = []
for user in users:
    response = iam.create_user(UserName=user)
    created_users.append(response['User']['UserName'])

print('Users created:', ','.join(created_users))

#=================================================================================================================================================================

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

# Create role
iam.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=json.dumps(assume_role_policy) #AssumeRolePolicyDocument must be a JSON string.
)
# Print confirmation on console
print('Role created:', role_name)

#=================================================================================================================================================================

# Function to create and attach an IAM policy
def create_and_attach_policy(policy_name, policy_document):
  response = iam.create_policy(
      PolicyName=policy_name,
      PolicyDocument=json.dumps(policy_document)
  )
  iam.attach_role_policy(
      RoleName=role_name,                                         
      PolicyArn=response['Policy']['Arn']
  )
  return response['Policy']['PolicyName']

# Policy document that allows read-only access to S3 and full access to EC2 
policy1 = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:Get*",
        "s3:List*",
        "s3:Describe*",
        "ec2:*"
      ],
      "Resource": "*"
    }
  ]
}

# Policy document that denies IAM user creation
policy2 = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "iam:CreateUser",
      "Resource": "*"
    }
  ]
}

# Function implementation
created_policies = []
created_policies.append(create_and_attach_policy('s3_ro_ec2_full_policy', policy1))   #### PUT IN YOUR DESIRED POLICY NAME ####
created_policies.append(create_and_attach_policy('deny_create_user_policy', policy2)) #### PUT IN YOUR DESIRED POLICY NAME ####

# Print the policy names joined in a single line
print('Policies created and attached to role:', ','.join(created_policies))

#=================================================================================================================================================================

s3_key = 'iam-configuration.json'                          ####Chose your s3 key####

# Define the IAM configuration to store in S3
config = {
    'Users': users,
    'Role': role_name, 
    'Policies': ['s3_ro_ec2_full_policy', 'deny_create_user_policy'] #### PUT IN THE POLICY NAMES ####
}

# Put the IAM configuration in the specified S3 bucket
s3.put_object(Bucket=bucket_name, Key=s3_key, Body=json.dumps(config))

# Print a confirmation message
print(f"IAM configuration stored in S3 bucket: {bucket_name}/{s3_key}")