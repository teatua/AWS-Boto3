# Import necessary libraries
import boto3
import json

# Specify the SSO profile name that you want to use
sso_profile_name = "boto3"

# Create a Boto3 session using the SSO profile
session = boto3.Session(profile_name=sso_profile_name)

# Create an IAM client using the custom SSO profile
iam = session.client('iam')

# Function to create and attach an IAM policy
def create_and_attach_policy(policy_name, policy_document):
  response = iam.create_policy(
      PolicyName=policy_name,
      PolicyDocument=json.dumps(policy_document)
  )
  iam.attach_role_policy(
      RoleName="Ninja",                                         #### PUT IN YOUR DESIRED ROLE NAME ####
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

# Create and attach the policies
created_policies = []
created_policies.append(create_and_attach_policy('s3_ro_ec2_full_policy', policy1))   #### PUT IN YOUR DESIRED POLICY NAME ####
created_policies.append(create_and_attach_policy('deny_create_user_policy', policy2)) #### PUT IN YOUR DESIRED POLICY NAME ####

# Print the policy names joined in a single line
print('Policies created and attached to role:', ','.join(created_policies))