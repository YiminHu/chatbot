import json
import boto3



def lambda_handler(event, context):
    # TODO implement
    # return event
    client = boto3.client('lex-runtime','us-east-1')
    response = client.post_text(
    botName='DiningConciergeChatbot',
    botAlias='firstChatbot',
    userId='nlpchat',
    sessionAttributes={
        'string': ''
    },
    requestAttributes={
        'string': ''
    },
    inputText= str(event['message']).lower()
    )

    return {
        "statusCode": 200,
        "body": response['message'],
        "headers": { 
            "Access-Control-Allow-Origin": "*" 
        }
    }
    

