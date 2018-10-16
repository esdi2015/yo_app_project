from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from . utils import GENDER_CHOICES, DEFAULT_USER_GENDER


User=get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default=DEFAULT_USER_GENDER)
    points = models.IntegerField(default=0, blank=True, null=True)
    rank = models.IntegerField(default=0, blank=True, null=True)
    region = models.CharField(max_length=200, blank=True)
    interests = models.ManyToManyField('common.Category', blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    subscribe = models.BooleanField(default=False)
    phone = models.CharField(max_length=16,blank=True,null=True)
    age = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

