import json
import random

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from . import config
from .models import Meme, Pun, MessengerUser, Joke
from .methods import get_sequece_ratio, send_main_menu
from .jobs import fetch_meme, fetch_joke, fetch_pun

from bot.methods import extract_payload, extract_text_message, extract_recipient_id, is_payload, is_text_message
from bot.models import QuickReply, NotificationType
from bot.bot import MessengerBot

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@csrf_exempt
def CustomFetchView(request, category):
    if request.method == 'GET':
        if category == 'meme':
            count = fetch_meme()
        elif category == 'joke':
            count = fetch_joke()
        elif category == 'pun':
            count = fetch_pun()

        return HttpResponse("".join(["New ", str(count), " ", category, " items added !"]))

    else:
        return HttpResponse("You need to make a GET request to perform fetch operation")


class FacebookWebhookView(View):
    @ method_decorator(csrf_exempt)  # required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    ###  DECLARING BOT HERE ###
    ###########################
    bot = MessengerBot(access_token=config.ACCESS_TOKEN,
                       api_version=config.API_VERSION)
    ###########################
    ###########################

    def get(self, request, *args, **kwargs):
        # hub_mode   = request.GET.get('hub.mode')
        hub_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')

        if hub_token != config.ACCESS_TOKEN:
            return HttpResponse('Error, invalid token', status=403)
        return HttpResponse(hub_challenge)

    def post(self, request, *args, **kwargs):
        print("\n", request.body, "\n")

        payload = json.loads(request.body.decode('utf-8'))
        recipient_id = extract_recipient_id(payload)

        try:
            user = MessengerUser.objects.get(facebook_id=recipient_id)
            print(" >>> MessengerUser fetched !!")
        except:
            user = MessengerUser(facebook_id=recipient_id)
            user.save()
            print(" >>> Created new messenger user ...")

        if is_payload(payload):
            payload_text = extract_payload(payload)
            request.session['prev_payload_text'] = payload_text

            if payload_text == 'SEND_MEME_PAYLOAD':
                """ send a random meme """

                queryset = Meme.objects.all()
                try:
                    meme = queryset[user.meme_count]
                    self.bot.send_image_url(
                        recipient_id=recipient_id, image_url=meme.url)
                    user.meme_count += 1
                    user.save()

                except:
                    self.bot.send_text_message(
                        recipient_id=recipient_id, message="There are no new memes available. Come back later tomorrow for more <3 ")

            elif payload_text == 'MEME_TEMPLATE_PAYLOAD':
                """ ask for the caption (MENTION THE MEME CAPTION/TEXT) """
                self.bot.send_text_message(
                    recipient_id=recipient_id, message="Mention the meme template's caption/text (eg. Why are you running?)")

            elif payload_text == 'TELL_JOKES_PAYLOAD':
                """ send a random joke """
                queryset = Joke.objects.all()

                try:
                    joke = queryset[user.joke_count]

                    self.bot.send_text_message(
                        recipient_id=recipient_id, message=joke.title)
                    self.bot.send_text_message(
                        recipient_id=recipient_id, message=joke.content)
                    user.joke_count += 1
                    user.save()

                except:
                    self.bot.send_text_message(
                        recipient_id=recipient_id, message="No new jokes available now. Come back tomorrow for more.")

            elif payload_text == 'SEND_PUN_PAYLOAD':
                queryset = Pun.objects.all()

                try:
                    pun = queryset[user.pun_count]

                    self.bot.send_text_message(
                        recipient_id=recipient_id, message=pun.title)
                    self.bot.send_text_message(
                        recipient_id=recipient_id, message=pun.content)
                    self.bot.send_image_url(
                        recipient_id=recipient_id, image_url=pun.url)
                    user.pun_count += 1
                    user.save()

                except:
                    self.bot.send_text_message(
                        recipient_id=recipient_id, message="No pun available. Come back tomorrow for more.")

        # # Handle Text Messages Here
        # if is_text_message(payload) and not is_payload(payload):
        #     print(" . . . . . . . . . . . . . ")
        #     print(payload)
        #     print(" = = = == == = = = == = = == = = = == ")
        #     print(request.session.get('prev_payload_text'))
        #     print(" = = = == == = = = == = = == = = = == ")

        #     text_message = extract_text_message(payload)
        #     prev_payload = request.session.get('prev_payload_text')

        # #    if prev_payload == 'MEME_TEMPLATE_PAYLOAD':

        #     queryset = MemeTemplate.objects.all()
        #     self.bot.send_text_message(
        #         recipient_id=recipient_id, message="Hope these are the templates you asked for. If didn't find what you were looking, let us know.")
        #     for item in queryset:
        #         if get_sequece_ratio(text_message, item.caption) >= config.SEQUENCE_RATIO:
        #             self.bot.send_image_url(
        #                 recipient_id=recipient_id, image_url=item.get_absolute_image_url)
        #     try:
        #         #del request.session['prev_payload_text']
        #         pass
        #     except:
        #         pass

        #    else:

        self.bot.send_quick_reply(
            recipient_id=recipient_id, text="What would you like me to do?", quick_reply=send_main_menu())

        return HttpResponse("Success", status=200)
