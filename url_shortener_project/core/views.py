from django.shortcuts import (
    render, redirect, reverse
)
from django.http import(
    HttpResponseRedirect,
)
from django.conf import (
    settings,
)
from django.views import View
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


class HomeView(View):
    form_class = URLForm
    current_shortened_url = None
    current_original_url = None
    template_name = 'core/home.html'
    initial = None

    def get(self, request):
        self.current_shortened_url = request.session.get(
            'current_shortened_url'
        )
        self.current_original_url = request.session.get(
            'current_original_url'
        )
        if self.current_shortened_url:
            del request.session['current_shortened_url']
        if self.current_original_url:
            self.initial = {
                'url_to_shorten': self.current_original_url
            }
            del request.session['current_original_url']

        form = self.form_class(initial=self.initial)
        return render(
            request,
            self.template_name,
            context={
                'form': form,
                'shortened_url': self.current_shortened_url,
            }
        )

    def post(self, request):
        form = self.form_class(request.POST)
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
            request.session['current_shortened_url'] = shortened_url
            request.session['current_original_url'] = original_url
            return redirect(
                reverse(
                    'core:home',
                )
            )
    
        return render(
            request,
            self.template_name,
            context={
                'form': form
            }
        )


def redirect_to_original(request, path):
    shortened_url = HOST + path
    original_url = URL.objects.get(
        shortened_url=shortened_url
    ).original_url

    return HttpResponseRedirect(original_url)
