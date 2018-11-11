import json
import datetime
import boto3

def lambda_handler(event, context):
    print(context)
    client = boto3.client('lex-runtime')
    response={
      "messages": [
      ]
    }
    message_template={
      "type": "string",
      "unstructured": {
        "id": "",
        "text": "",
        "timestamp":"" 
      }
    }
    # message=message_template
    now = datetime.datetime.now()
    text=event["messages"][0]["unstructured"]["text"]
    print(text)
    resp=client.post_text(botName='Jarvis',
      botAlias='Beta',
      userId=event["messages"][0]["unstructured"]["id"],
      inputText=text)
    print(resp)
    message=message_template
    message["unstructured"]["id"]=event["messages"][0]["unstructured"]["id"]
    message["unstructured"]["text"]=resp["message"]
    message["unstructured"]["timestamp"]=now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%02d' % (now.microsecond / 10000))
    response["messages"].append(message)
    return response