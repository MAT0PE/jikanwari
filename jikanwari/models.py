from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core import validators

COLOR_CHOICES = (
    ('#FFFFFF', '白'),
    ('#1E90FF', '青'),
    ('#FF4500', '赤'),
    ('#32CD32', '緑'),
    ('#FFFF4A', '黄色'),
)

class Class(models.Model):
    name = models.CharField(max_length=20)
    url = models.TextField(blank=True)
    memo = models.TextField(blank=True)
    day_period = models.CharField(max_length=6, default='', help_text='ex) Mon1, Wed4')
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#FFFFFF')
    #user
    def __str__(self):
        return self.name

PERIOD_CHOICES = (
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
)

class Settings(models.Model):
    sat = models.BooleanField(default=False)
    sun = models.BooleanField(default=False)
    s1 = models.TimeField(default=None, blank=True, null=True)
    e1 = models.TimeField(default=None, blank=True, null=True)
    s2 = models.TimeField(default=None, blank=True, null=True)
    e2 = models.TimeField(default=None, blank=True, null=True)
    s3 = models.TimeField(default=None, blank=True, null=True)
    e3 = models.TimeField(default=None, blank=True, null=True)
    s4 = models.TimeField(default=None, blank=True, null=True)
    e4 = models.TimeField(default=None, blank=True, null=True)
    s5 = models.TimeField(default=None, blank=True, null=True)
    e5 = models.TimeField(default=None, blank=True, null=True)
    s6 = models.TimeField(default=None, blank=True, null=True)
    e6 = models.TimeField(default=None, blank=True, null=True)
    s7 = models.TimeField(default=None, blank=True, null=True)
    e7 = models.TimeField(default=None, blank=True, null=True)
    open_link = models.BooleanField(default=False)
    period = models.IntegerField(default=4, validators=[validators.MinValueValidator(4), validators.MaxValueValidator(7)], choices=PERIOD_CHOICES)

class Assignments(models.Model):
    deadline = models.DateTimeField()
    subject = models.CharField(max_length=20)
    label = models.CharField(max_length=10)
    memo = models.TextField()
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#FFFFFF')
    # notification = models.BooleanField(default=False)
    def __str__(self):
        return self.subject
