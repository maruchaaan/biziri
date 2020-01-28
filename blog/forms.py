from django import forms

from .models import Sentence

class SentenceForm(forms.ModelForm):

    class Meta:
        model = Sentence
        fields = ('text',)
