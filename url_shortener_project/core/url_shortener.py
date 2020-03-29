import random
import string

from django.conf import (
    settings,
)
from .models import URL


def url_shortener(original_url):
    shortened_url = settings.ALLOWED_HOSTS[0] + ':8000/'
    for _ in range(6):
        shortened_url += random.choice(
            string.ascii_letters + string.digits
        )
    while True:
        try:
            URL.objects.get(shortened_url=shortened_url)
            # if such URL already exists, make another one
            shortened_url = ''.join(
                random.shuffle(
                    list(shortened_url)
                )
            )
        except URL.DoesNotExist:
            return shortened_url
