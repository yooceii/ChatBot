import json
import datetime

def lambda_handler(event, context):
    templates={
      "hello":"Hi, How are you?",
      "hi":"Hi there, I'm Jarvis and you?",
      "good":"That's awesome.",
      "bye":":)"
    }
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
    message=message_template
    now = datetime.datetime.now()
    text=event["messages"][0]["unstructured"]["text"].lower()
    message=message_template
    message["unstructured"]["id"]="12313"
    message["unstructured"]["text"]=templates.get(text,"I don't understand what are you saying")
    message["unstructured"]["timestamp"]=now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%02d' % (now.microsecond / 10000))
    response["messages"].append(message)
    return response
