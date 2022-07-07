from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from .models import Song

class SongListView(ListView):
    model = Song


class SongDetailView(DetailView):
    model = Song
