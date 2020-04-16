import os
import requests


def post_to_slack(event, context):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

    data = { "text": "An event happened."}
    requests.post(slack_webhook_url, json=data)

    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
        }