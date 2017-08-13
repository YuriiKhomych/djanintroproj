from django.db import models

from django.conf import settings

from datetime import datetime


class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(default=datetime.now, blank=True)
    from_city = models.CharField(max_length=255)
    destination_city = models.CharField(max_length=255)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator')

    def __str__(self):
        return '{} | {}'.format(self.title, self.creator, self.from_city, self.destination_city)
