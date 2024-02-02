# Import all the modules and Libraries
import boto3

# Open Session
session = boto3.Session(profile_name='boto3')
# Open IAM Console
iam = session.client(service_name="iam")

# List IAM users
response = iam.list_users()
users = response.get('Users', [])

if not users:
    print("None")
else:
    for user in users:
        print(user['UserName'])