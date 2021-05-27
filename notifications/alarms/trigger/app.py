import json
import boto3


class Alarm:
    def __init__(self, alarm: dict):
        self.silo = alarm.get("silo", "unknown")
        self.severity = alarm.get("severity", "unknown")
        self.threshold = alarm.get("threshold", -1)
        self.parameter = alarm.get("parameter", "unknown")
        self.value = alarm.get("value", -1)
        self.phone = alarm.get("phone", None)
        self.email = alarm.get("email", None)


def build_message(silo, severity, parameter, threshold, value):
    return f"""SiouxSilos ALERT!
    Silo involved: {silo}
    Severity: {severity.capitalize()}
    Cause: Parameter over threshold
    {parameter.capitalize()} expected to be lower than {threshold} but is {value}
    """


def notify_topic(topic: str, alarm: Alarm):
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=topic,
        Subject="SiouxSilosAlert",
        Message=build_message(
            alarm.silo, alarm.severity, alarm.parameter,
            alarm.threshold, alarm.value
        )
    )
    print(response)


def lambda_handler(event, context):
    topic_arn = "arn:aws:sns:eu-central-1:240595528763:SiouxSilosAlerts"

    body = event.get("body", {})
    alarm = Alarm(body)

    notify_topic(topic_arn, alarm)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "Topic alerted successfully"
        }),
    }
