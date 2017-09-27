from django.db import models
from django.core.exceptions import ValidationError

from django.conf import settings

from datetime import datetime

def validate_rating(value):
    if value > 10 or value < 0:
        raise ValidationError("%(value)s is not a valid rating. Rating must be 0 >= value <= 10",
                              params={"value": value}, )


class Trip(models.Model):
    from_city = models.CharField(max_length=255)
    destination_city = models.CharField(max_length=255)
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    passengers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='passengers')
    max_passengers = models.CharField(max_length=255)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='driver')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} | {}'.format(self.driver, self.from_city, self.destination_city)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="username_of_commenter")
    trip = models.ForeignKey(Trip, related_name="commented_trip", null=True)
    positive = models.TextField(blank=True, null=True)
    negative = models.TextField(blank=True, null=True)
    body = models.TextField()
    rating = models.DecimalField(max_digits=3,
                                 decimal_places=1,
                                 blank=True,
                                 null=True,
                                 validators=[validate_rating,])
    date = models.DateTimeField(auto_now_add=True, null=True)
    edit_date = models.DateTimeField(blank=True, null=True)
    edit_amount = models.IntegerField(default=0)

    class Meta:
        unique_together = ("author", "trip")

    def __str__(self):
        return "{} {} {}".format(self.author, self.trip, self.rating)


