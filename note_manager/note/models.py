from __future__ import unicode_literals

import uuid, logging

from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from django.urls import reverse


def upload_location(instance, filename):
    return u"%s/%s" % (instance.id, filename)


class Post(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    uuid_boolean = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=120)
    content = models.TextField()
    favourite = models.BooleanField(default=False)
    CATEGORY_CHOICES = [
        ('Ссылка', 'Ссылка'),
        ('Заметка', 'Заметка'),
        ('Памятка', 'Памятка'),
        ('TO DO', 'TO DO'),
    ]
    category = models.CharField(
        max_length=7,  # why?
        choices=CATEGORY_CHOICES,
    )
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     #self.id = models.AutoField(primary_key=True)
    #     #self.id = None #########
    #     #self.id = 0
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        # return reverse("posts:detail", kwargs={"id": self.id})
        return reverse("note:detail", kwargs={"id": self.id})

    def get_uuid_url(self):
        #id = uuid.uuid4()
    #    return reverse("note:detail", kwargs={self.id}) #вернуть на id чтобы работало
       # return '/note/{}/'.format(self.unique_id)

        return reverse("note:publish", kwargs={"unique_id": self.unique_id})  # вернуть на id чтобы работало


    class Meta:
        ordering = ["-created", "-updated"]
# Create your models here.
