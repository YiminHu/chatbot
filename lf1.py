import json
import boto3
import logging
import os
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # TODO implement
    slots = event['currentIntent']['slots']
    message = slots['Location'] + "_" + slots['Cuisine'] + "_" + slots['Dining_time'] + "_" + slots['Number_People'] + "_" + slots['Phone']
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/419611625149/usermessage'
    response = sqs.send_message(
        QueueUrl = queue_url,
        MessageBody = message
        )
    
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "SSML",
                "content": "Gotcha! Will send to your phone with our recommendations!"
            },
        }
    }

