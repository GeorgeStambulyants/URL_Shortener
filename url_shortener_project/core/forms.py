from django import forms
from .models import FriendlyURL, URL


class URLForm(forms.Form):
    url_to_shorten = forms.URLField(label='URL to shorten')
    word_for_slug = forms.SlugField(required=False)

    def check_unique_slug(self, slug, object_list):
        for obj in object_list:
            if obj.friendly_shortened_url.endswith(slug):
                raise forms.ValidationError('Such slug already exists')

    def clean_word_for_slug(self):
        cd = self.cleaned_data
        word_for_slug = cd['word_for_slug']
        original_url = cd['url_to_shorten']

        if word_for_slug:    
            try:
                url_obj = URL.objects.get(original_url=original_url)
                friendly_url_objs = FriendlyURL.objects.exclude(original_url=url_obj.pk)
                self.check_unique_slug(word_for_slug, friendly_url_objs) 
            except URL.DoesNotExist:
                friendly_url_objs = FriendlyURL.objects.all()
                self.check_unique_slug(word_for_slug, friendly_url_objs)
        return word_for_slug
