from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Song


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = "__all__"