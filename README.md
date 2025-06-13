Project 5: The AWS Messenger - Automated Notifications with Boto3 and SNS

Objective:
To write and run a Python script that creates an SNS topic, subscribes your email to it, publishes a test message, and then cleans up all created resources.

Core Technologies:

    Python
    Boto3
    AWS SNS (Simple Notification Service)

Instructions

    Prepare Your Environment:
        Create a new project directory (e.g., project5-sns).
        Inside that directory, create and activate a new Python virtual environment (venv).
        Install Boto3: pip install boto3.
        Make sure your AWS credentials are set up (e.g., you've run aws configure).

    Set Up IAM Permissions:
        The AWS user or role you are using needs permissions to manage SNS. For this learning project, attach the AWS-managed policy named AmazonSNSFullAccess to your user or role.

    Save the Script:
        Take the code from the "Project 5: SNS Notifier Script" canvas above and save it in your project directory as a Python file (e.g., sns_project5_script.py).

    IMPORTANT: Update Script Configuration:
        Open the sns_project5_script.py file.
        Find the "Configuration" section at the top.
        Update the TARGET_EMAIL variable with an email address you can access.
        Python

    # Change this line
    TARGET_EMAIL = "your-real-email@example.com" 

Execute the Script:

    Open your terminal, navigate to your project directory, and make sure your virtual environment is active.
    Run the script:
    Bash

    python sns_project5_script.py

Follow On-Screen and Email Instructions:

    The script will start and immediately send a subscription confirmation request to your email.
    The terminal will pause and print: >>> Please check your email inbox and click the 'Confirm subscription' link.
    Go to your email inbox. Find the email from "AWS Notifications" and click the confirmation link.
    The script will automatically detect the confirmation after a few seconds.
    Once confirmed, it will publish a test message. You will receive a second email with the subject "Test Notification from Boto3 Project 5".
    The script will then pause one last time, waiting for you to press Enter in the terminal before it proceeds to delete the SNS topic and subscription it created.
