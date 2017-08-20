from django.db import models

from django.conf import settings

from datetime import datetime


class Trip(models.Model):
    from_city = models.CharField(max_length=255)
    destination_city = models.CharField(max_length=255)
    date = models.DateField(default=datetime.now, blank=True)
    time = models.TimeField(default=datetime.now, blank=True)
    passengers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='passengers')
    max_passengers = models.CharField(max_length=255)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='driver')

    def __str__(self):
        return '{} | {}'.format(self.driver, self.from_city, self.destination_city)
