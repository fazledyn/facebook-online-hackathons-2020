from django.contrib import admin
from .models import Pun, Meme, Joke, MessengerUser

admin.site.register(Pun)
admin.site.register(Meme)
admin.site.register(Joke)
admin.site.register(MessengerUser)
