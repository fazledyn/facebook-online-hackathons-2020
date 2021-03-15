from django.db import models

# Create your models here.

class FacebookUser(models.Model):
    facebook_id =   models.CharField(max_length=100, default='00000000000')
    name        =   models.CharField(max_length=100, null=True)
    phone       =   models.CharField(max_length=15, null=True)
    event       =   models.CharField(max_length=150, default='This person is not affiliated in any event')
    token       =   models.CharField(max_length=50, null=True)
    credential  =   models.ImageField(upload_to='credentials', null=True, blank=True)

    def get_event_data(self):
        return self.event

    def __str__(self):
        return self.name + "\n" + self.facebook_id