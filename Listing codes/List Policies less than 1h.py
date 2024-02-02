# Import necessary libraries
import boto3
import datetime
from dateutil import tz

# Specify the SSO profile name that you want to use
sso_profile_name = "boto3"

# Create a Boto3 session using the SSO profile
session = boto3.Session(profile_name=sso_profile_name)

# Create an IAM client using the custom SSO profile
iam = session.client('iam')

# Calculate the timestamp for one hour ago in UTC
one_hour_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)

# List IAM policies
response = iam.list_policies()
policies = response.get('Policies', [])

recent_policies = []

for policy in policies:
    create_date = policy['CreateDate']
    
    # Convert create_date to UTC timezone
    create_date = create_date.replace(tzinfo=tz.tzlocal()).astimezone(tz.tzutc())
    
    # Ensure that the policy was created within the past hour
    if create_date > one_hour_ago:
        recent_policies.append(policy['PolicyName'])

if not recent_policies:
    print("None")
else:
    for policy_name in recent_policies:
        print(policy_name)