import random
import string
from django.conf import settings


def url_shortener(original_url):
    shortened_url = settings.ALLOWED_HOSTS[0] + ':8000/'
    for _ in range(6):
        shortened_url += random.choice(string.ascii_letters)
    
    return shortened_url