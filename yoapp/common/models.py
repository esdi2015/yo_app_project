from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db.models.signals import post_save
from . import receivers
from django.contrib.auth import get_user_model
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from . utils import ROLES, DEFAULT_USER_ROLE


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, blank=True, unique=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    role = models.CharField(max_length=50, choices=ROLES, default=DEFAULT_USER_ROLE)
    creator_id = models.SmallIntegerField(default=0)
    fb_id = models.CharField(max_length=100, blank=True, unique=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.get_full_name()


class Category(MPTTModel):
    category_name = models.CharField(max_length=64, unique=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['category_name']

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __unicode__(self):
        return self.category_name

    def __str__(self):
        return self.category_name


class Region(models.Model):
    region_name = models.CharField(max_length=200)

    class Meta:
        ordering = ('region_name',)
        verbose_name = "region"
        verbose_name_plural = "regions"

    def __str__(self):
        return self.region_name



post_save.connect(receivers.create_auth_token, sender=get_user_model())

