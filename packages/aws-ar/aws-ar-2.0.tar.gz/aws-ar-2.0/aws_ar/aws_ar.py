import argparse
import subprocess

def assume_role(arn, profile, new_profile):
    
    sts_output = subprocess.check_output(['aws', 'sts', 'assume-role', '--role-arn', arn, '--role-session-name', 'AssumeRoleSession', '--profile', profile])

    sts_output_lines = sts_output.decode().splitlines()
    for line in sts_output_lines:
        if 'AccessKeyId' in line:
            access_key = line.split(':')[1].strip().strip(',').strip('"').strip('"')
        elif 'SecretAccessKey' in line:
            secret_key = line.split(':')[1].strip().strip(',').strip('"').strip('"')
        elif 'SessionToken' in line:
            session_token = line.split(':')[1].strip().strip(',').strip('"').strip('"')

    subprocess.run(['aws', 'configure', 'set', 'aws_access_key_id', access_key, '--profile', new_profile])
    subprocess.run(['aws', 'configure', 'set', 'aws_secret_access_key', secret_key, '--profile', new_profile])
    subprocess.run(['aws', 'configure', 'set', 'aws_session_token', session_token, '--profile', new_profile])

def main():
    parser = argparse.ArgumentParser(description='AWS Assume Role Utility')
    parser.add_argument('--role-arn', required=True, help='ARN of the role to assume')
    parser.add_argument('--profile', help='Name of the profile to use for assuming the role (default: default)')
    parser.add_argument('--new-profile', required=True, help='Name of the new profile to create')

    args = parser.parse_args()

    assume_role(args.role_arn, args.profile or 'default',args.new_profile)

    print(f'New profile {args.new_profile} configured with assumed role credentials.')

if __name__ == "__main__":
    main()
