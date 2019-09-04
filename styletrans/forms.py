from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from styletrans.models import Picture
from django.forms import ModelForm, Textarea

MAX_UPLOAD_SIZE = 2500000

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('picture',)
    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture

