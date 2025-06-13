import boto3
from botocore.exceptions import ClientError
import time

# --- Configuration ---
AWS_REGION = "us-east-1"

# You MUST have access to this email inbox to confirm the subscription.
TARGET_EMAIL = "t.w.x.y@hotmail.com" 

SNS_TOPIC_NAME = "boto3-project5-notifications"

# Initialize SNS client
sns_client = boto3.client('sns', region_name=AWS_REGION)

# --- Helper Functions ---

def create_sns_topic(topic_name):
    """
    Creates an SNS topic and returns its ARN.
    """
    print(f"\nAttempting to create or get SNS topic: {topic_name}...")
    try:
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response['TopicArn']
        print(f"Successfully got topic ARN: {topic_arn}")
        return topic_arn
    except ClientError as e:
        print(f"Error creating SNS topic: {e}")
        return None

def subscribe_email_to_topic(topic_arn, email_address):
    """
    Subscribes an email address to an SNS topic.
    """
    print(f"\nSubscribing '{email_address}' to topic '{topic_arn}'...")
    try:
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email_address
        )
        print("Subscription request sent successfully.")
        print(">>> Please check your email inbox and click the 'Confirm subscription' link.")
        return True
    except ClientError as e:
        print(f"Error subscribing email: {e}")
        return False

def get_confirmed_subscription_arn(topic_arn, email_address):
    """
    Polls SNS to find the confirmed subscription ARN for a given email.
    This is the corrected way to handle email subscription confirmation.
    """
    print("\nWaiting for subscription confirmation...")
    timeout_seconds = 180  # Wait for up to 3 minutes
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        try:
            paginator = sns_client.get_paginator('list_subscriptions_by_topic')
            for page in paginator.paginate(TopicArn=topic_arn):
                for sub in page.get('Subscriptions', []):
                    if sub.get('Endpoint') == email_address:
                        # A confirmed subscription will have a real ARN.
                        # A pending one will have the string 'PendingConfirmation'.
                        if "PendingConfirmation" not in sub['SubscriptionArn']:
                            print("Subscription confirmed successfully!")
                            return sub['SubscriptionArn'] # Return the REAL ARN
            
            print("  Subscription is still pending... please check your email and click the confirmation link.")
            time.sleep(10) # Wait 10 seconds before checking again

        except ClientError as e:
            print(f"Error while checking subscriptions: {e}")
            return None
            
    print("Timed out waiting for subscription confirmation.")
    return None

def publish_message_to_topic(topic_arn, subject, message):
    """
    Publishes a message to the specified SNS topic.
    """
    print(f"\nPublishing message to topic '{topic_arn}'...")
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
        message_id = response['MessageId']
        print(f"Message published successfully! Message ID: {message_id}")
        return message_id
    except ClientError as e:
        print(f"Error publishing message: {e}")
        return None

def cleanup(topic_arn, subscription_arn):
    """
    Unsubscribes from and deletes the SNS topic.
    """
    print("\n--- Initiating Cleanup ---")
    try:
        # Only try to unsubscribe if we have a valid, confirmed ARN.
        if subscription_arn:
            print(f"Unsubscribing '{subscription_arn}'...")
            sns_client.unsubscribe(SubscriptionArn=subscription_arn)
            print("Unsubscribed successfully.")
        else:
            print("Skipping unsubscribe because subscription was not confirmed.")

        if topic_arn:
            print(f"Deleting topic '{topic_arn}'...")
            sns_client.delete_topic(TopicArn=topic_arn)
            print("Topic deleted successfully.")
            
    except ClientError as e:
        print(f"Error during cleanup: {e}")

# --- Main Script Logic ---
def main():
    """Main function to run the SNS demo."""
    print("--- Starting Project 5: Boto3 and AWS SNS ---")

    topic_arn = None
    confirmed_subscription_arn = None
    
    try:
        # 1. Create the SNS topic
        topic_arn = create_sns_topic(SNS_TOPIC_NAME)
        if not topic_arn:
            return

        # 2. Subscribe your email to the topic
        if not subscribe_email_to_topic(topic_arn, TARGET_EMAIL):
            raise Exception("Subscription request failed, proceeding to cleanup.")
        
        # 3. Wait for confirmation and get the real ARN
        confirmed_subscription_arn = get_confirmed_subscription_arn(topic_arn, TARGET_EMAIL)
        
        if not confirmed_subscription_arn:
            print("Could not confirm subscription. You will not receive the published message.")
        else:
            # 4. Publish a message to the topic
            subject = "Test Notification from Boto3 Project 5"
            message = "Hello!\n\nThis is an automated message sent from a Python script using AWS SNS.\n\nIt looks like the test was successful."
            publish_message_to_topic(topic_arn, subject, message)
            print("\nCheck your email inbox for the notification message!")

        # Pause before cleaning up
        input("\nPress Enter to proceed with cleanup (unsubscribe and delete topic)...")

    except Exception as e:
        print(f"An error occurred in the main script logic: {e}")
    finally:
        # 5. Clean up the created resources
        cleanup(topic_arn, confirmed_subscription_arn)

    print("\n--- Project 5 script finished. ---")

if __name__ == "__main__":
    main()