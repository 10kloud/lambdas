import json
import boto3


def register_email(email):
    sns_client = boto3.client('sns')
    topic_arn = "arn:aws:sns:eu-central-1:240595528763:SiouxSilosAlerts"
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol="email",
        Endpoint=email,
        ReturnSubscriptionArn=False
    )
    print(response)


def register_sms(phone_number):
    sns_client = boto3.client('sns')
    topic_arn = "arn:aws:sns:eu-central-1:240595528763:SiouxSilosAlerts"
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol="sms",
        Endpoint=phone_number,
        ReturnSubscriptionArn=False
    )
    print(response)


def lambda_handler(event, context):
    body = event.get("body", {})

    email = body.get("email", None)
    phone = body.get("phone", None)
    message = "Cannot register the user"

    if email:
        register_email(email)
        message = "User registered successfully by Email"

    if phone:
        register_sms(phone)
        message = "User registered successfully by SMS"

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": message
        }),
    }
