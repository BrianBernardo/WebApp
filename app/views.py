from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Song
from django.urls import reverse_lazy

class HomePageView(TemplateView):
    template_name = 'app/home.html'


class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class songPageView(ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'app/song.html'

class songDetailsView(DetailView):
    model = Song
    content_object_name = 'song'
    template_name = 'app/song_details.html'

class songCreateview(CreateView):
    model = Song
    fields = ['title', 'artist', 'genre', 'release_date']
    template_name = 'app/addSong.html'

class songUpdateView(UpdateView):
    model = Song
    fields = ['title', 'artist', 'genre', 'release_date']
    template_name = 'app/updateSong.html'

class songDeleteview(DeleteView):
    model = Song
    template_name = 'app/deleteSong.html'
    success_url = reverse_lazy('song')