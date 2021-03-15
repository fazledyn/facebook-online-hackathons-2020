from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View

from .models import DebugMessage
from bot.models import FacebookUser

import webhook.config as config
import webhook.quick_reply as reply
import sys, json, requests

"""
The root is the main directory under the project which handles basic communication with
Messenger Platform. 

The configurations are stored in the config.py file.
"""

# Secondary Methods

# Webhook Views
"""
def root(request, *args, **kwargs):

    if request.method == 'GET':
        
        hub_mode        = request.GET.get('hub.mode')
        hub_token       = request.GET.get('hub.verify_token')
        hub_challenge   = request.GET.get('hub.challenge')
        
        if hub_token != config.VERIFY_TOKEN:   
            return HttpResponse('Error, invalid token', status_code=403)
    
        return HttpResponse(hub_challenge)

    else:
        print(request.body)

        incoming_message = json.loads(request.body.decode('utf-8'))

        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    fb_user_id = message['sender']['id']
                    fb_user_txt = message['message'].get('text')

                    if fb_user_txt:
                        new_msg = DebugMessage.objects.create(content=fb_user_txt)
                        new_msg.save()

                        send_message(fb_user_id, fb_user_txt)

        return HttpResponse("Success", status=200)
"""


class FacebookWebhookView(View):
    @method_decorator(csrf_exempt) # required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) #python3.6+ syntax    


    def get(self, request, *args, **kwargs):
        hub_mode   = request.GET.get('hub.mode')
        hub_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if hub_token != config.VERIFY_TOKEN:
            return HttpResponse('Error, invalid token', status_code=403)
        return HttpResponse(hub_challenge)
            

    def post(self, request, *args, **kwargs):
        print("\n", request.body, "\n")

        incoming_message = json.loads(request.body.decode('utf-8'))
        
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                fb_user_id = message['sender']['id']

                if 'message' in message:

                    if 'quick_reply' in message['message']:
                        # this is a quick reply type message
                        payload_text = message['message']['quick_reply']['payload']

                        if payload_text == 'GET_STARTED_PAYLOAD':
                            reply.get_started(fb_user_id)

                        if payload_text == 'FIND_EVENT_PAYLOAD':
                            reply.find_events(fb_user_id)

                        if payload_text == 'CREDENTIALS_PAYLOAD':
                            reply.credential(fb_user_id)

                        if payload_text == "MY_ACCOUNT_PAYLOAD":
                            reply.my_account(fb_user_id)

                    if 'text' in message['message']:
                        user_send_text = message['message'].get('text')
                        arr = user_send_text.split('|')                  

                        if arr[0] == 'ZYX_TOKEN':
                            token_data = arr[1]
                            reply.register_token(fb_user_id, token_data)

                        elif user_send_text == 'menu' or 'help':
                            reply.show_menu(fb_user_id)

                        elif "thanks" or "thank" in user_send_text.lower():
                            reply.send_message(fb_user_id, "You are welcome!")

        return HttpResponse("Success", status=200)
