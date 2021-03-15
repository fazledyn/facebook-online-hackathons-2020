from django.db import models


class MemeTemplate(models.Model):
    image = models.ImageField(upload_to='image/meme_template')
    caption = models.CharField(max_length=600)

    @property
    def get_absolute_image_url(self):
        return "https://citrogen.herokuapp.com" + self.image.url

    def __str__(self):
        return self.caption


class Meme(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=100)
    source = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)


class Joke(models.Model):
    title = models.CharField(max_length=800)
    content = models.TextField()

    def __str__(self):
        return self.content


class Pun(models.Model):
    title = models.CharField(max_length=800)
    content = models.TextField()
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class MessengerUser(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    facebook_id = models.CharField(max_length=50)
    meme_count = models.IntegerField(default=0)
    joke_count = models.IntegerField(default=0)
    pun_count = models.IntegerField(default=0)

    def __str__(self):
        return self.facebook_id
