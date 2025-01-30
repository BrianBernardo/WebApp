from django import forms
from .models import Song, Mood, Rating, SongComment, Playlist

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre', 'release_date', 'moods', 'youtube_embed_code']      
        exclude = ['user']

    moods = forms.ModelMultipleChoiceField(
        queryset=Mood.objects.all(),
        widget=forms.CheckboxSelectMultiple  
    )
    youtube_embed_code = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Right click on the video, copy embed code then paste it here', 'rows': 7}),
        required=False  
    )


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']

    rating = forms.ChoiceField(
        choices=[(i, f'{i} Star') for i in range(1, 6)],  
        widget=forms.Select,  
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = SongComment
        fields = ['content']

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'songs']

    songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=forms.CheckboxSelectMultiple,  
        required=False  
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['songs'].label_from_instance = lambda song: f"{song.title} - {song.artist}"