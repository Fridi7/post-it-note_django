import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse


class Post(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    uuid_boolean = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=120)
    content = models.TextField()
    favourite = models.BooleanField(default=False)
    CATEGORY_CHOICES = [
        ('LNK', 'Ссылка'),
        ('NT', 'Заметка'),
        ('MEM', 'Памятка'),
        ('TD', 'TO DO'),
        ('ETC', 'Другое'),
    ]
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='NT')
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("note:detail", kwargs={"id": self.pk})

    def get_uuid_url(self):
        return reverse("note:publish", kwargs={"unique_id": self.unique_id})

    class Meta:
        ordering = ["-created", "-updated"]
