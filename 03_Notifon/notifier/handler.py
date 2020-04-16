import json


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
        }