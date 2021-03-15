import os, json, requests
import webhook.config as config

from bot.models import FacebookUser
from hackathon.settings import MEDIA_ROOT, BASE_DIR

# main function for handling communication
def message_sender(response_data):

    endpoint = config.ENDPOINT
    status = requests.post(
                    endpoint,
                    headers={"Content-Type": "application/json"},
                    data=response_data)
    
    print(status.json())
    return status.json()
# --------------------------------------------


def send_message(fb_user_id, user_message):

    endpoint = config.ENDPOINT
    response_msg = json.dumps({"recipient":{"id":fb_user_id}, "message":{"text":user_message}})
    message_sender(response_msg)


def show_menu(fb_user_id):
    response = json.dumps(
        {
            "recipient": {
                "id": fb_user_id 
            },
            "messaging_type": "RESPONSE",
            "message":{
                "text": "What would you like to do?",
                "quick_replies": [
                {
                    "content_type":"text",
                    "title":"Get Started",
                    "payload":"GET_STARTED_PAYLOAD"
                },
                {
                    "content_type":"text",
                    "title":"Find Events",
                    "payload":"FIND_EVENT_PAYLOAD"
                },
                {
                    "content_type":"text",
                    "title":"Credential",
                    "payload":"CREDENTIALS_PAYLOAD"
                },
                {
                    "content_type":"text",
                    "title":"My Account",
                    "payload":"MY_ACCOUNT_PAYLOAD"
                }
                ]
            }
        }
    )
    message_sender(response)


def get_started(fb_user_id):
    message = "Send the token given to you here and if it gets matched, you will be verified soon. For any kind of issue, you can type 'help'/'menu'"
    send_message(fb_user_id, message)


def find_events(fb_user_id):
    user_list = FacebookUser.objects.filter(facebook_id=fb_user_id)
    
    for user in user_list:
        event_details = user.get_event_data()

    response = json.dumps(
        {
            "recipient": {
                "id": fb_user_id 
            },
            "messaging_type": "RESPONSE",
            "message":{
                "text": event_details,
            }
        }
    )
    message_sender(response)


def credential(fb_user_id):
    user_list = FacebookUser.objects.filter(facebook_id=fb_user_id)

    credential_url = ""
    credential_full_path = ""

    if user_list is not None:

        for user in user_list:
            credential_path = user.credential.url
        
        credential_full_path = "https://zyx-the-bot.herokuapp.com" + credential_path
        print(credential_full_path)

        response = json.dumps(
            {
                "recipient": {
                    "id": fb_user_id 
                },
                "messaging_type": "RESPONSE",
                "message":{
                    'attachment': {
                    'type': "image",
                    'payload': {
                        'url': credential_full_path
                    }
                }
                }
            }
        )
        message_sender(response)
    
    else:
        send_message(fb_user_id, "You aren't verified yet !")


def register_token(fb_user_id, token_data):

    user_list = FacebookUser.objects.filter(token=token_data)
    response = "Error"

    if user_list is None:
        # no user has been found
        response = "You have entered the token incorrectly."
    
    else:
        for user in user_list:
            if user.facebook_id == "00000000000":
                # user hasn't been verified
                if user.token == token_data:
                    user.facebook_id = fb_user_id
                    user.save()
                    response = "You have been verified"

            elif user.facebook_id == fb_user_id:
                # user already verified
                response = "You are already verified"

    send_message(fb_user_id, response)

def my_account(fb_user_id):

    user_list = FacebookUser.objects.filter(facebook_id=fb_user_id)
    user_info = ""

    if user_list is not None:
        for user in user_list:
            user_info += "Facebook ID: " + user.facebook_id + "\n"
            user_info += "User token: " + user.token + "\n"
    else:
        user_info = "User account info error"
    
    send_message(fb_user_id, user_info)