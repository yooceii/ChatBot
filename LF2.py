import requests
import json
import boto3
from datetime import datetime
from time import mktime

client = boto3.client('sns')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DiningSuggestions')

def lambda_handler(event, context):
    print(event)
    for record in event['Records']:
        resp=search(record['messageAttributes']["Location"]["stringValue"],record['messageAttributes']["Cuisine"]["stringValue"],record['messageAttributes']["Date"]["stringValue"],record['messageAttributes']["DiningTime"]["stringValue"])
        number=record['messageAttributes']["PhoneNumber"]["stringValue"]
        ID = record['messageId']
        Message = json.dumps(record)
        result = format(resp.json())
        store_DynamoDB(ID, Message, "\n".join(result))
        send_SMS(number,result)
        # print(results)
    return 
        

def search(location,categories,date,diningTime):
    time=int(mktime(datetime.strptime(date+" "+diningTime, '%Y-%m-%d %H:%M').timetuple()))
    payload={"location":location,"categories":categories,"open_at":time,"limit":5}
    headers = {
        'Authorization': 'Bearer %s' % 'wyThAM96643tyL-4wdLA3HI9F8p8XpeNvc7CdDIhvbYoBPYuGaZWffyOKf9lxStBtwSYrQ2mHFLHp8tzyFGjyESIaeHPvi02D4h2G0sK76Xk6pXdYBYtwe1R8ODkW3Yx',
    }
    return requests.get("https://api.yelp.com/v3/businesses/search",headers=headers,params=payload)
    
def format(json):
    results=[]
    for restaurant in json["businesses"]:
        result=[]
        name=restaurant["name"]
        location="".join(restaurant["location"]["display_address"])
        results.append(f'{name}, located at {location}')
    return [j[0]+j[1] for j in zip([f'{i}. ' for i in range(1,len(results)+1)],results)]
    
def send_SMS(number, text):
    client.publish(
        PhoneNumber = '+'+number,
        Message = "\n".join(text)
    )

def store_DynamoDB(ID, Message, Suggestion):
    table.put_item(
        Item = {
            'ID': ID,
            'Message': Message,
            'Suggestion': Suggestion
        }
    )