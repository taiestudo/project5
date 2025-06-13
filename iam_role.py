import boto3
from botocore.exceptions import ClientError
import json
import time

# --- Configuration ---
AWS_REGION = "us-east-1"
ROLE_NAME = "Project5-SNS-Access-Role"

# Initialize IAM client
iam_client = boto3.client('iam', region_name=AWS_REGION)

def create_sns_access_role():
    """
    Creates an IAM Role that can be assumed by EC2 and grants it full access to SNS.
    This function is idempotent. If the role already exists, it does nothing.
    """
    print(f"\nChecking for IAM Role: {ROLE_NAME}...")
    try:
        # Check if the role already exists to avoid errors
        iam_client.get_role(RoleName=ROLE_NAME)
        print(f"Role '{ROLE_NAME}' already exists. No action needed.")
        return True
    except iam_client.exceptions.NoSuchEntityException:
        print(f"Role '{ROLE_NAME}' not found. Creating...")

    # Define the trust policy document, allowing the EC2 service to assume this role.
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }

    try:
        # Create the IAM role with the trust policy
        iam_client.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="A role that grants full access to SNS for Project 5"
        )
        
        print(f"Role '{ROLE_NAME}' created. Attaching SNS policy...")
        
        # Attach the AWS-managed policy for full SNS access
        iam_client.attach_role_policy(
            RoleName=ROLE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/AmazonSNSFullAccess"
        )
        
        print("Policy 'AmazonSNSFullAccess' attached successfully.")
        # Allow a moment for IAM changes to propagate
        time.sleep(10) 
        return True

    except ClientError as e:
        print(f"Error creating role or attaching policy: {e}")
        return False

if __name__ == "__main__":
    print("--- Starting IAM Setup for SNS Project ---")
    if create_sns_access_role():
        print("\nIAM Role setup complete. The user/principal running the main SNS script")
        print("should now be configured with these permissions or assume this role.")
    else:
        print("\nIAM Role setup failed.")
