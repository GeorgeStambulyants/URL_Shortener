import random
import string


def url_shortener(original_url):
    shortened_url = 'http://localhost:8000/'
    for _ in range(6):
        shortened_url += random.choice(string.ascii_letters)
    
    return shortened_url