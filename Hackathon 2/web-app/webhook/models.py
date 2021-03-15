from django.db import models

# Create your models here.
class DebugMessage(models.Model):
    content = models.TextField(max_length=1000)

    def __str__(self):
        return self.content