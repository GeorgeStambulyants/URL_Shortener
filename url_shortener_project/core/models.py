from django.db import models


class URL(models.Model):
    original_url = models.URLField(max_length=200, unique=True)
    shortened_url = models.URLField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.original_url} => {self.shortened_url}'


class FriendlyURL(models.Model):
    friendly_shortened_url = models.SlugField(max_length=100, blank=True, unique=True)
    original_url = models.ForeignKey(
        to=URL, on_delete=models.CASCADE, related_name='friendly_url'
    )
    is_active = models.BooleanField(default=True)
