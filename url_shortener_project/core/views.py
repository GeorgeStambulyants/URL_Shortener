from django.shortcuts import (
    render, redirect,
)
from django.http import(
    HttpResponseRedirect,
)
from django.conf import (
    settings,
)
from .forms import (
    URLForm,
)
from .url_shortener import (
    url_shortener,
)
from .models import (
    URL,
)


HOST = settings.ALLOWED_HOSTS[0] + ':8000/'


def home(request):
    shortened_url = None
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            original_url = cd['url_to_shorten']
            try:
                shortened_url = URL.objects.get(
                    original_url=original_url
                ).shortened_url
            except URL.DoesNotExist:
                shortened_url = url_shortener(original_url)
                URL.objects.create(
                    original_url=original_url,
                    shortened_url=shortened_url,
                )
    else:
        form = URLForm()
    
    return render(
        request,
        'core/home.html',
        context={
            'form': form,
            'shortened_url': shortened_url,
        }
    )


def redirect_to_original(request, path):
    shortened_url = HOST + path
    original_url = URL.objects.get(
        shortened_url=shortened_url
    ).original_url

    return HttpResponseRedirect(original_url)
