import json
import math
import dateutil.parser
import datetime
import time
import os
import boto3

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='Jarvis')

def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    print('lambda')
    return dispatch(event)
    
def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    
    if intent_name == 'GreetingIntent':
        return greeting(intent_request)
        
    elif intent_name == 'DiningSuggestionsIntent':
        return diningSuggestions(intent_request)
        
    elif intent_name == 'ThankYouIntent':
        return thankyou(intent_request)

def greeting(intent_request):
    response = {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': 'Hi there, how can I help?'
            }
        }
    }
    return response

def diningSuggestions(intent_request):
    location = get_slots(intent_request)['Location']
    cuisine = get_slots(intent_request)['Cuisine']
    date = get_slots(intent_request)['Date']
    dining_time = get_slots(intent_request)['DiningTime']
    number = get_slots(intent_request)['NumberOfPeople']
    phone_number = get_slots(intent_request)['PhoneNumber']
    source = intent_request['invocationSource']
    
    slots = get_slots(intent_request)
    
    validate_result = validate_dining_suggestions(
        location, cuisine, date, dining_time, number, phone_number)
    if not validate_result['isValid']:
        slots[validate_result['violatedSlot']] = None
        return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validate_result['violatedSlot'],
                               validate_result['message'])
    
    push_message(intent_request)
    
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': "You’re all set. Expect my recommendations shortly! Have a good day." 
                  })
        

def thankyou(intent_request):
    response = {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': 'You’re welcome.'
            }
        }
    }
    return response

def validate_dining_suggestions(
    location, cuisine, date, dining_time, number, phone_number):
    cuisines = ['chinese', 'japnese', 'indian', 'mexican']
    
    if cuisine is not None and cuisine.lower() not in cuisines:
        return build_validation_result(False, 'Cuisine',
        'We do not have {}, would you like a different cuisine?'.format(cuisine))
    
    if number is not None:
        if not is_valid_people_number(number):
            return build_validation_result(False, 'NumberOfPeople',
            'Sorry, please input the positive number of people.')
            
    
    return build_validation_result(True, None, None)
    

def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            'isValid': is_valid,
            'violatedSlot': violated_slot
        }
    
    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

def is_valid_people_number(number):
    try:
        if int(number) <= 0:
            return False
        return True
    except ValueError:
        return False
    
def get_slots(intent_request):
    return intent_request['currentIntent']['slots']
    
def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response

def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

def push_message(intent_request):
    
    location = get_slots(intent_request)['Location']
    cuisine = get_slots(intent_request)['Cuisine']
    date = get_slots(intent_request)['Date']
    dining_time = get_slots(intent_request)['DiningTime']
    number = get_slots(intent_request)['NumberOfPeople']
    phone_number = get_slots(intent_request)['PhoneNumber']
   
    message_attributes = {
        'Location': {
        'StringValue': location,
        'DataType': 'String.Location'
        },
        'Cuisine': {
        'StringValue': cuisine,
        'DataType': 'String.Cuisine'
        },
        'Date': {
        'StringValue': date,
        'DataType': 'String.Date'
        },
        'DiningTime': {
        'StringValue': dining_time,
        'DataType': 'String.DiningTime'
        },
        'NumberOfPeople': {
        'StringValue': number,
        'DataType': 'Number.NumberOfPeople'
        },
        'PhoneNumber': {
        'StringValue': phone_number,
        'DataType': 'Number.PhoneNumber'
        }
    }
    
    response = queue.send_message(
    MessageBody='Jarvis Dining Suggestions',
    MessageAttributes = message_attributes)
    
    return response