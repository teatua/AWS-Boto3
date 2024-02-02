# AWS IAM configuration using boto3

Using code 🐍 , we will create three AWS IAM Users, one AWS IAM
Role and two AWS IAM Policies meeting the following requirements:

- The two policies should be attached to the role.
- One policy should allow:
    - Read only - S3,
    - Full Access - EC2
- One policy should Deny:
    - IAM user creation
- The users you create should be able to assume the Role as long as they have an MFA
authenticated session.
- Store all config in a S3 bucket so that you have a master copy

## Understanding

There are 3 main ways in which you can interact with your AWS environment:

1) AWS Console (graphical interface)
2) AWS Command Line interface (CLI)
3) AWS Software Development Kit (SDK)

Each have their own pros and cons.
When administrating small businesses, the 1st option may be easier to adopt. But as a company grows, administration can become repetitive, and some features may be lacking, thus the need to use AWS programmatically.

### Prerequisites
 
- Password Manager such as [KeepassXC](https://keepassxc.org/)
- MFA (software-based authenticator such as [Google](https://support.google.com/accounts/answer/1066447?hl=en&co=GENIE.Platform%3DAndroid) or [Microsoft](https://www.microsoft.com/en-us/security/mobile-authenticator-app) Authenticator or a a hardware authentication device such as [YubiKey](https://www.yubico.com/))
- Python version 3.8 or later
- Boto3
- AWS Account
- AWSCLIV2

### Optional

- IDE ([VsCode](https://code.visualstudio.com/) or [Pycharm](https://www.jetbrains.com/pycharm/))
- AWS Toolkit (free tier AI Auto-Suggestions, Security Scan)

### Setup and Installation

We will assume you already have your own Password Manager and MFA authenticator.

#### Python

To use the AWS SDK for python, you will need version 3.8 or later of Python
(https://www.python.org/downloads/)

Check if already installed by opening a terminal

    python --version

If you are new to Python and do not receive any response to the above command, it would be preferable to select __ADD Python to Path__ in the installation process

Once the installation process completed, take a break or restart your computer. The required versions of Python we are using comes with PIP (Pip Install Packages), the package manager for Python.

#### Boto3

[Boto3]((https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)) is the name of the AWS SDK for python. To install it, paste the following command in a terminal

    pip install boto3

This command will install the boto3 library for Python



#### AWS Account

Register for a [free tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all) account, this will require a credit card. _I do not guarantee this project to run for free, please inform yourself on AWS charges relating the services we will be using prior proceeding._

Once logged into the AWS management console, it would be preferable to setup Multi-Factor-Authentication (MFA) to your root account. 

- For this click on your username at the top right corner of your window and select "Security credentials"
![Alt text](<Images/Select Credential security.png>)

- Next click on "Assign MFA device" and follow the instructions
![Alt text](<Images/Assign MFA.png>)

Congrats ! You have added a layer of security to your new AWS account 😀 Now I did mention this project is not guaranteed to be free but you can start monitoring your costs, let's create our first budget !

- Search for "AWS Budgets" in the AWS searchbar
![Alt text](<Images/Search AWS Budgets.png>)

- AWS should guide you through creating your first zero spend budget, if not click on the "Create Budget" button
![Alt text](<Images/Create Budget.png>)

- You can keep the default selection as seen bellow, make sure to enter your email address in Email recipients, then click create
![Alt text](<Images/My zero budget template.png>)

With the basics out of the way, let's create a user for our boto3 script to run from.

- At first, I was going to create a user in Identity and Access Management (IAM) and generate an access key to link with AWS CLI, although AWS gave me the following warning:
![Alt text](<Images/CLI Warning.png>)

- Let's follow the recommendation and search for "IAM identity Center" in the search bar
![Alt text](<Images/search IAM identity Center.png>)

IAM Identity Center (previously known as AWS SSO) will need to be enabled, for this an Organization will also need to be created. AWS Organizations service is a way to congregate multiple AWS accounts, as larger businesses tend to have multiple accounts (test and production, isolated services) and while AWS also promots doing so, this initially created bottlenecks such as having to create a user in each accounts for one single engineer, or having to bookwork multiple bills. Therefore the need for AWS Organizations.
_Note that an AWS account can only belong to 1 AWS Organization._

IAM Identity Center works with all AWS Accounts in an AWS Organizations, enabling a centralized Identity and Access Management source. 

Now that we have created an Organization linking our AWS account and enabled IAM Identity Center, we will need to choose an identity source, select "Choose your identity source" from the IAM Identity Center Dashboard
![Alt text](<Images/Choose your identity source.png>)

To keep this simple, we will be opting for the Identity Center directory which works with AWS service: IAM Identity Center. 
![Alt text](<Images/Identity Center directory.png>)

- Active directory is good for businesses with on prem or cloud Microsoft AD environments.  _(If you have a paid subscription to Microsoft 365 though, you also have a free Azure AD)_

- External identity provider is best when using multiple applications and requiring a congregated source for Identity & Access Management. Users can access applications such as AWS, Slack, Workforce, Microsoft 365 and more with one single account, and Administrators are able to manage the access levels from a single source (provided the tool has proper mapping for identity control). This technology can be built custom, but if a business has enough ressources to do so, this probably means it will start falling under compliance regulations. The fast & easy way for cashing corporates is to chose a commercial provider, some of the most well known are Okta & Microsoft Azure AD (both meeting PCI-DSS level 1 compliance at the time of releasing this project).


Now that we have chosen our identity source, let's jump into IAM Identity Center --> __Settings__ and select __Authentication__, from there we will be able to __Configure__ MFA for our boto3 user (Security First!)
![Alt text](<Images/IAM IC MFA configure.png>)

To follow best practices, we will ensure:

- Prompt users for MFA
    - Every time they sign in (always-on)
- Users can authenticate with these MFA types
    - Security keys and built-in authenticators and/or Authenticator apps
- If a user does not yet have a registered MFA device
    - Require them to register an MFA device at sign in

We can now create our boto3 user in __IAM Identity Center__ by navigating to __Users__ and clicking on __Add user__
![Alt text](<Images/Add User.png>)

Fill-in the required details for your boto3 user and click __next__
![Alt text](<Images/User information.png>)

We can skip the groups and finalise user creation. _You will receive an email to setup password and instructions to connect to the AWS access portal which should also require MFA setup following our MFA configuration in the previous step_

Next, we will create our first __Permission Set__ located under __Multi-account Permissions__ in your IAM Identity Center side navigation
![Alt text](<Images/Create Permission.png>)

Select __Custom permission set__
![Alt text](<Images/Custom Permission Set.png>)

As AWS recommends, we will procede with __Inline policy__. Under which we will select __+ Add new statement__ from where we will choose the IAM service
![Alt text](<Images/Inline Policy statement IAM service.png>)

Select the following actions:
- CreateRole
- CreateUser
- CreatePolicy
- AttachRolePolicy
![Alt text](<Images/Inline Policy IAM actions.png>)

Naviguate back to __All services__
![Alt text](<Images/Inline policy all services.png>)

Choose __S3__
![Alt text](<Images/Inline Policy statement S3 service.png>)

Select the following actions:
- CreateBucket
- PutObject
![Alt text](<Images/Inline policy S3 Actions.png>)

Click on the __Add Ressource__ and select __All Ressources__
![Alt text](<Images/Inline Policy Add Ressource.png>)

Notice the Warning for missing version? We can manually add this in the statement, simply copy paste as follow:

    "Version": "2012-10-17",
![Alt text](<Images/Inline Policy version.png>)

Click __Next__ and finalise your first permission set !

- [Reference for building IAM JSON policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html) 

- Policies can be tested with [IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html), in the [IAM Policy Simulator](https://policysim.aws.amazon.com/home/index.jsp#) (limited to success and failed responses) or in a test environment.

We will now assign our user to our aws account through __IAM Identity Center__ --> __Multi-account permissions__ --> __AWS Accounts__
![Alt text](<Images/Assign user.png>)

Select the boto3 user you have created and click next
![Alt text](<Images/Assign user next.png>)

Select the newly created permission set, click next and submit
![Alt text](<Images/Assign permission set.png>)

#### AWSCLIV2

Download and install AWSCLIV2: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Have a break or restart your machine, then open a Terminal and configure the AWS CLI to authenticate users with the AWS IAM Identity Center (IAM Identity Center) token provider configuration.

    aws configure sso

We will Choose boto3 as our session name

    SSO session name (Recommended): boto3

You will need to login your user to the AWS portal with the provided URL given during your user setup. Under your AWS account, select __Command line or programmatic access__
![Alt text](<Images/cli or programmatic access.png>)

Following AWS recommendation, we will copy our SSO Start URL and Region under our matching Operating System, to further use it in our AWS CLI authentication with AWS IAM Identity Center
![Alt text](<Images/Copy SSO Start URL and SSO Region.png>)

    SSO start URL [None]: (paste your url)
    SSO region [None]: (paste your region)
    SSO registration scopes [sso:account:access]: (skip enter)
You will receive an __Authorization Request from your browser with an 8 character code to match with the one given in your terminal. Confirm, Continue, and Allow
![Alt text](<Images/Authorisation request.png>)

Back to your terminal, you may notice the following

    The only role available to you is: "Permission set name"
    Using the role name "Permission set name"

This is because IAM Identity Center Permission sets do not create Users in a given AWS Account but Roles (Can be found in your AWS account roles, under IAM, something in the line of AWSReservedSSO...)

    CLI default client Region [None]: (skip/enter)    
    CLI default output format [None]: (skip/enter)
    CLI profile name ["Permission set name"-"accountid"]: boto3

Your AWSCLIV2 is now configured to work with your AWS user. Try and connect using the following command

    aws sso login --profile boto3 

If you chose a different CLI profile name, replace boto3 with your chosen one. Once more you may be redirected to your browser for an Authorization request.

Following this your terminal should display 

    Successfully logged into Start URL: "your URL"

We can now start using boto3, RG boto3.py will be the assembly of all the codes necessary to complete the exercise. It contains comments to explain each sections of the code, some parts of the code will need to be changed to your needs.

## Q&A

Propose a solution for providing access for users in a large to medium size company’s
AWS environment.

Things to think about:

● How would it work with many users?

● Many Roles?

● Many Accounts?

Using AWS IAM Identity Center, we can provide users with a single sign-on experience to all AWS accounts. We can have all users, groups, and permission policies grouped in one bundle.

This can facilitate:

- Lifecycle Management: Establish a process for adding, modifying, and removing users and permissions as they join, change roles, or leave the organization. 

- Review and Audits

AWS Organizations service control policies (SCPs) can be attached to accounts as a safety measure to protect critical services.

Implement robust AWS CloudTrail and Amazon CloudWatch Logs for auditing and monitoring. These services track all API requests and provide insights into who did what, where, and when.





## Authors

  - **Ryan Grand** 




## Acknowledgments

  - Hat tip to the Xero team for providing me with such an opportunity to learn

