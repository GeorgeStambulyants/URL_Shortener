from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.conf import settings
from django.views import View

from .forms import URLForm
from .url_shortener import url_shortener, friendly_url_shortener
from .models import URL, FriendlyURL


HOST = settings.ALLOWED_HOSTS[0] + ':8000/'


class HomeView(View):
    form_class = URLForm
    current_shortened_url = None
    current_original_url = None
    current_friendly_url = None
    template_name = 'core/home.html'
    initial = None

    def retrieve_current_urls_from_session(self, request):
        self.current_shortened_url = request.session.get(
            'current_shortened_url'
        )
        self.current_original_url = request.session.get(
            'current_original_url'
        )
        self.current_friendly_url = request.session.get(
            'current_friendly_url'
        )

        if self.current_friendly_url:
            del request.session['current_friendly_url']
        if self.current_shortened_url:
            del request.session['current_shortened_url']
        if self.current_original_url:
            self.initial = {
                'url_to_shorten': self.current_original_url
            }
            del request.session['current_original_url']

    def save_current_urls_in_session(self, request, \
            original_url, shortened_url, friendly_url):

        request.session['current_shortened_url'] = shortened_url
        request.session['current_original_url'] = original_url
        request.session['current_friendly_url'] = friendly_url

    def get(self, request):
        self.retrieve_current_urls_from_session(request)
        form = self.form_class(initial=self.initial)
        return render(
            request,
            self.template_name,
            context={
                'form': form,
                'shortened_url': self.current_shortened_url,
                'friendly_url': self.current_friendly_url,
            }
        )
    
    def save_new_friendly_url_and_return_it(self, url, word_for_slug):
        friendly_url = friendly_url_shortener(word_for_slug)
        friendly_url_object = FriendlyURL.objects.create(
                friendly_shortened_url=friendly_url,
                original_url=url
            )
        return friendly_url_object.friendly_shortened_url

    def get_friendly_url(self, url, word_for_slug):
        if word_for_slug:
            for obj in url.friendly_url.all():
                if obj.friendly_shortened_url.endswith(word_for_slug):
                    return obj.friendly_shortened_url

            return self.save_new_friendly_url_and_return_it(url, word_for_slug)
        try:
            return url.friendly_url.all()[0].friendly_shortened_url
        except IndexError:
            return None

    def get_shortened_url(self, url):
        return url.shortened_url

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            original_url = cd['url_to_shorten']
            word_for_slug = cd['word_for_slug']
            try:
                url = URL.objects.get(
                    original_url=original_url
                )
                shortened_url = self.get_shortened_url(url)
                friendly_url = self.get_friendly_url(url, word_for_slug)
            except URL.DoesNotExist:
                shortened_url = url_shortener()
                url = URL.objects.create(
                        original_url=original_url,
                        shortened_url=shortened_url,
                    )
                if word_for_slug:
                    friendly_url = friendly_url_shortener(word_for_slug)
                    FriendlyURL.objects.create(
                        friendly_shortened_url=friendly_url,
                        original_url=url,
                    )
                else:
                    friendly_url = None
            
            self.save_current_urls_in_session(
                request, original_url, shortened_url, friendly_url,
            )

            return redirect(reverse('core:home'))
    
        return render(
            request, self.template_name, context={'form': form}
        )


def redirect_to_original(request, path):
    shortened_url = HOST + path
    try:
        url = URL.objects.get(
            shortened_url=shortened_url
        )
        original_url = url.original_url
    except URL.DoesNotExist:
        try:
            url = FriendlyURL.objects.get(
                friendly_shortened_url=shortened_url
            )
            original_url = url.original_url.original_url
        except FriendlyURL.DoesNotExist:
            return HttpResponseBadRequest('Bad request')

    return HttpResponseRedirect(original_url)
