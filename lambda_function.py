
"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from twilio.rest import TwilioRestClient


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "MyProblemIsIntent":
        return set_problem(intent, session)
    elif intent_name == "WhatsMyProblemIntent":
        return get_help(intent, session)
    elif intent_name == "ContactIntent":
        return contact(intent, session)
    elif intent_name == "MyProblemIsIntent":
        return set_problem(intent, session)
    elif intent_name == "GiveAdviceIntent": 
        return get_help(intent, session)
    elif intent_name == "SprainIntent":
        return treat_sprain(intent, session)
    elif intent_name == "NosebleedIntent":
        return treat_nosebleed(intent, session)
    elif intent_name == "PapercutIntent":
        return treat_papercut(intent, session)
    elif intent_name in ["BurnsIntent", "ChestPainIntent", "DizzyIntent", "DehydratedIntent", "CongestedIntent", "FeverIntent", "AbnormalPulseIntent", "ArmTingleIntent","ChillsIntent"]:
        return treat_serious(intent, session)
    elif intent_name == "SymptomsIntent":
        return diagnose(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome, I'm Baylexa, your personal healthcare assistant. What can I do for you?"
    reprompt_text = "Are you in danger? Do you want help?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def contact(intent, session):
        card_title = intent['name']
        session_attributes = {}
        reprompt_text = None
        account_sid = "AC39d9722bca359c3885bd8e876492859d"
        auth_token  = "222f8028aa78ffbdecbb558badf6db93"
        client = TwilioRestClient(account_sid, auth_token)
        speech_output = "Something went wrong, sorry."
        should_end_session = True
        if "Message" in intent['slots']:
                m = intent['slots']['Message']['value']
                try:
                        message = client.messages.create(body=m,
                        to="+16478367351",    # Replace with your phone number
                        from_="+15675100423") # Replace with your Twilio number
                        print(message.sid)
                        speech_output = "I contacted your physician"
                except twilio.TwilioRestException as e:
                        print(e)
        return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))

def get_help(intent, session):
    card_title = intent['name']
    session_attributes = {}
    reprompt_text = None
    should_end_session = True

    if "Problems" in session.get('attributes', {}):
        problem = session['attributes']['Problems']
        speech_output = "Your problem is " + problem
    else:
        speech_output = "I'm not sure what your problem is. You can tell me your problem"
    #

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def set_problem(intent, session):
    #sets what kind of problem is going on
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Problems' in intent['slots']:
        problem = intent['slots']['Problems']['value']
        session_attributes = create_problem_attributes(problem)
        speech_output = "Okay, I see you're having a" + problem + "today"
        print(problem)
        reprompt_text = "You can tell me your problem. I got your back"

    else:
        speech_output = "So you're not having" + problem + "today?"
        reprompt_text = "I'm not quite sure what the problem is. Let me know how I can help"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def create_problem_attributes(problem):
    return {"Problems": problem}
    
## quick and dirty
def treat_sprain(intent, session):
    session_attributes = {}
    reprompt_text = None
    card_title = intent['name']
    speech_output = "Rest the sprained area. Put some ice on it. Do not apply ice directly on the skin. Call an ambulance if there is significant swelling."
    should_end_session = True
    print('sprain works??')
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def treat_nosebleed(intent, session):
    session_attributes = {}
    reprompt_text = None
    card_title = intent['name']
    speech_output = "Sit up straight and lean forward slightly. Pinch your nose firmly with your thumb and forefinger. If the bleeding does not stop in ten minutes, call an ambulance."
    should_end_session = True
    print('nosebleed works??')
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
def treat_papercut(intent, session):
    session_attributes = {}
    reprompt_text = None
    card_title = intent['name']
    speech_output = "Do not worry, it is only a flesh wound. Rinse the cut with clean water and use a bandaid to prevent infection."
    should_end_session = True
    print('papercut works??')
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
## srs bizness

def treat_serious(intent, session):
    session_attributes = {}
    reprompt_text = None
    card_title = intent['name']
    speech_output = "Please list all your symptoms"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def diagnose(intent, session):
    session_attributes = {}
    reprompt_text = None
    card_title = intent['name']
    should_end_session = True
    speech_output = "Fallback"
    print("checking symptoms")
    if "Symptoms" in intent['slots']:
        usersymps = intent['slots']['Symptoms']['value']
        print(usersymps)
        pt_symSet = set(usersymps.split())
        print(pt_symSet)
        flu_symptoms = set(['dizziness', 'nausea', 'fever', 'chills', 'dehydration', 'congestion'])
        MI_symptoms = set(['chestpain', 'leftarmtingling', 'dizziness', 'nausea', 'abnormal pulse'])
        def compare(set1, set2, set3):
            set1 = pt_symSet
            set2 = flu_symptoms
            set3 = MI_symptoms
            print(set1)
            print(set.__len__(set1 & set2))
            flu_score = set.__len__(set1 & set2)/set.__len__(set2)
            MI_score = set.__len__(set1 & set2)/set.__len__(set3)
            print(flu_score)
            print(MI_score)
            if flu_score > 0.60: 
                speech_output = "You most likely have the flu. Contact your physician as soon as possible."
            elif MI_score > 0.25: 
                speech_output = "You most likely are experiencing a heart attack. Call nine one one immediately"
            else: 
                speech_output = "I was unable to diagnose you. If your symptoms get worse, please call your physician."
            return speech_output
        speech_output = compare(pt_symSet, flu_symptoms, MI_symptoms)
            
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
