from django import forms


class URLForm(forms.Form):
    url_to_shorten = forms.URLField(label='URL to shorten')
    word_for_slug = forms.SlugField(required=False)
