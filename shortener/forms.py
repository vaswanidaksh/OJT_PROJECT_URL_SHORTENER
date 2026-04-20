from django import forms
from .models import ShortURL


class ShortenerForm(forms.ModelForm):
    original_url = forms.URLField(
        widget=forms.URLInput(attrs={
            'class': 'url-input',
            'placeholder': 'Paste your long link here...'
        })
    )

    class Meta:
        model = ShortURL
        fields = ['original_url']

    def clean_original_url(self):
        """
        Custom validation: allow the form to accept URLs that already exist
        in the database. The duplicate check is handled in the view, not here.
        We just strip and return the URL.
        """
        url = self.cleaned_data['original_url'].strip()
        return url