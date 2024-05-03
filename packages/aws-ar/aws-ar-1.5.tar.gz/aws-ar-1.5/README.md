# AWS-AR: AWS Assume Role CLI Utility

AWS-AR is a command-line utility that simplifies the process of configuring assumed AWS IAM role credentials in your local AWS configuration files `($HOME/.aws/config and $HOME/.aws/credentials)`. This tool allows you to assume an IAM role and automatically update your AWS CLI configuration with the temporary security credentials obtained from the assumed role.

### Features

- Assume an AWS IAM role and obtain temporary security credentials.
- Update AWS CLI configuration files ($HOME/.aws/config and $HOME/.aws/credentials) with the assumed role credentials.
- Supports specifying the ARN of the IAM role, AWS CLI profile, and optionally creating a new profile for the assumed role.

### Installation

You can install AWS-AR using pip:

```bash
pip install aws-ar
```

### Usage

Assuming an IAM role and updating AWS CLI configuration:

```bash
aws-ar --assume-role-arn <role_arn> --profile <existing_profile> --set-new-profile <new_profile>
```
- <role_arn>: The ARN of the IAM role to assume.
- <existing_profile>: The name of the existing AWS CLI profile to use for assuming the role.
- <new_profile>: The name of the new profile to be created with the assumed role credentials.

### Example:

```bash
aws-ar --assume-role-arn arn:aws:iam::123456789012:role/MyRole --profile default --set-new-profile assumed-role
```

This command assumes the IAM role MyRole, uses the default AWS CLI profile for authentication, and creates a new profile named assumed-role with the assumed role credentials.