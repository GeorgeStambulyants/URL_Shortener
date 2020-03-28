from django.shortcuts import render
from .forms import URLForm
from .url_shortener import url_shortener
from .models import URL


def home(request):
    shortened_url = None
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            original_url = cd['url_to_shorten']
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
