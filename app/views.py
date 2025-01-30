from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Playlist, Song, Mood, Rating
from .forms import PlaylistForm, SongForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from .forms import CommentForm, RatingForm
from django.db.models import Avg


from django.urls import reverse_lazy


class IndexPageView(TemplateView):
    template_name = 'app/index.html'

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        moods = Mood.objects.all()  
        songs = []
        selected_mood = None

        if 'mood' in request.GET:
            selected_mood = request.GET['mood']
            mood = Mood.objects.filter(name=selected_mood).first()
            if mood:
                songs = Song.objects.filter(moods=mood)

        return render(request, 'app/home.html', {'moods': moods, 'songs': songs, 'selected_mood': selected_mood})



class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class songPageView(ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'app/song.html'
    ordering = ['-created_at']

class songDetailsView(DetailView):
    model = Song
    context_object_name = 'song'
    template_name = 'app/song_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = context['song']
        
        # Add the forms and ratings to the context
        context['comment_form'] = CommentForm()  # Add the comment form to the context
        context['comments'] = song.comments.all()  # Get all the comments for the song
        context['rating_form'] = RatingForm()  # Add the rating form to the context

        # Calculate the average rating for the song
        avg_rating = Rating.objects.filter(song=song).aggregate(Avg('rating'))['rating__avg']
        context['avg_rating'] = avg_rating if avg_rating else None  # Display average rating or None if no ratings

        # Check if the user has already rated the song
        user_rating = Rating.objects.filter(song=song, user=self.request.user).first()
        context['user_rating'] = user_rating.rating if user_rating else None  # Display user's rating if available

        return context

    def post(self, request, *args, **kwargs):
        song = self.get_object()
        comment_form = CommentForm(request.POST)
        rating_form = RatingForm(request.POST)

        # Handle the comment form submission
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.song = song
            comment.user = request.user
            comment.save()

        # Handle the rating form submission
        if rating_form.is_valid():
            # Ensure the user can only rate once
            if not Rating.objects.filter(song=song, user=request.user).exists():
                rating = rating_form.save(commit=False)
                rating.song = song
                rating.user = request.user
                rating.save()

        # After processing both forms, redirect back to the song details page
        return redirect('song_detail', pk=song.pk)
class songCreateview(CreateView):
    model = Song
    form_class = SongForm
    template_name = 'app/addSong.html'

    def form_valid(self, form):
        # Automatically set the user to the logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

class songUpdateView(UpdateView):
    model = Song
    form_class = SongForm
    template_name = 'app/updateSong.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Only allow the user to edit their own songs
        if obj.user != self.request.user:
            raise Http404("You do not have permission to edit this song.")
        return obj

class songDeleteview(DeleteView):
    model = Song
    template_name = 'app/deleteSong.html'
    success_url = reverse_lazy('song')
    
    def get_object(self, queryset=None):
        # Get the song object
        song = super().get_object(queryset)
        # Check if the current user is the owner of the song
        if song.user != self.request.user:
            raise HttpResponseForbidden("You are not allowed to delete this song.")
        return song
    

@login_required
def create_playlist(request):
    """Allows users to create a playlist."""
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user  # Assign the logged-in user as the owner
            playlist.save()
            form.save_m2m()  # Save many-to-many relationships (songs)
            return redirect("playlist_list")  # Redirect to playlist list
    else:
        form = PlaylistForm()
    return render(request, "app/create_playlist.html", {"form": form})


@login_required
def playlist_list(request):
    """Displays all playlists created by the logged-in user."""
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, "app/playlist_list.html", {"playlists": playlists})


@login_required
def playlist_detail(request, playlist_id):
    """Displays details of a single playlist, including its songs."""
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    return render(request, "app/playlist_detail.html", {"playlist": playlist})


@login_required
def edit_playlist(request, playlist_id):
    """Allows users to update their playlist (add or remove songs)."""
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    
    if request.method == "POST":
        form = PlaylistForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()
            return redirect("playlist_detail", playlist_id=playlist.id)  
    else:
        form = PlaylistForm(instance=playlist)

    return render(request, "app/edit_playlist.html", {"form": form, "playlist": playlist})


@login_required
def delete_playlist(request, playlist_id):
    """Allows users to delete their playlist."""
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    
    if request.method == "POST":
        playlist.delete()
        return redirect("playlist_list")

    return render(request, "app/delete_playlist.html", {"playlist": playlist})
    