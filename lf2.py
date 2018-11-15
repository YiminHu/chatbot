import json
import logging
import boto3
from botocore.vendored import requests
import sys
import urllib

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
API_KEY= 'fxkdam9nXhJujo9HPzoDUOdsUWFdqIh2D06dLQ74RA1flZkQ5BpUuT4IjhtF2XthkwY1pZcJF79EGS5yz82mK3vIiZEEnRAqRfom587YY9adtVSMkdG0Px3_7OzoW3Yx'
def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, urllib.parse.quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()
# Initialize logger and set log level
logger = logging.getLogger()
logger.setLevel(logging.INFO)
session = boto3.Session(
    region_name="us-east-1"
)
sns_client = session.client('sns')

def lambda_handler(event, context):
    usermessage = event["Records"][0]["body"]
    infolist = usermessage.split("_")
    url_params = {}
    url_params["location"] = infolist[0]
    url_params["term"] = infolist[1]
    suggestion = request(API_HOST,SEARCH_PATH,API_KEY,url_params)
    phone = infolist[4]
    
    #url_params[]
    # TODO implement
    """
    response = sns_client.publish(
        PhoneNumber="+1"+phone,
        Message=event["Records"][0]["body"],
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': 'SENDERID'
            },
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Promotional'
            }
        }
    )
    """
   
    
    response_str = "Hello! Here are my "+ url_params["term"]+ " restaurant suggestions for " + \
    infolist[3] + " people, for today at "+ infolist[2]+ " :" 
    for i in range(3):
        curstr = str(i+1)+". "
        curstr = curstr+suggestion["businesses"][i]['name']+" located at "+suggestion["businesses"][i]['location']['address1']+" "
        response_str = response_str + curstr
        
    logger.info(suggestion)
    print(suggestion)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DinningSuggestion')
    table.put_item(
        Item = {"userInfo":event["Records"][0]["body"],"suggestion":response_str}
        )
    print(table.creation_date_time)
    return {
        'statusCode': 200,
        'body': event["Records"][0]["body"]
    }

