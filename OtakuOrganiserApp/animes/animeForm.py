from django.forms import ModelForm
from .anime import Anime

class AnimeForm(ModelForm):
    class Meta:
        model = Anime 
        exclude = ('anime_photo',)

class EditAnimeForm(ModelForm):
    class Meta:
        model = Anime 
        exclude = ('anime_id', 'anime_photo')