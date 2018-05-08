import uuid
from django.db import models
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from django.core.validators import MaxValueValidator, MinValueValidator
import json
from django.db.models import (
    UUIDField,
    CharField,
    IntegerField,
    BigIntegerField,
    FloatField,
    ImageField
)

class Anime(models.Model):
    anime_id = models.AutoField(primary_key=True,  editable =False)
    name = CharField(max_length = 100)
    genre = CharField(max_length = 200)

    MOVIE = "Movie"
    TV = "TV"
    OVA = "OVA"
    ONA = "ONA"
    SPECIAL = "Special"

    GENRE_CHOICE = (
        (MOVIE, "Movie"),
        (TV, "TV"),
        (OVA, "OVA"),
        (ONA, "ONA"),
        (SPECIAL, "Special")
    )

    anime_type = CharField(
        max_length = 7,
        choices = GENRE_CHOICE,
        default = TV,
    )

    episodes = IntegerField()
    rating = FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10)], default = 0)
    members = BigIntegerField()

    anime_photo = ImageField(null = True, upload_to = 'img/profiles', verbose_name = "Anime Photo", default = "{% static 'img/placeholder.jpg' %}")

    class Meta:
        ordering = ('-rating',)
