from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .animes import Anime, AnimeForm, EditAnimeForm
import csv
import io
import logging
from django.urls import reverse
from django import forms
from .forms import RegistrationForm

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import json

import re
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def add_anime(request):
    animeForm = AnimeForm()

    if request.method == 'POST':
        animeForm = AnimeForm(request.POST)
        if animeForm.is_valid():
            anime = Anime()
            anime.name = animeForm.cleaned_data['name']
            anime.genre= animeForm.cleaned_data['genre']
            anime.anime_type = animeForm.cleaned_data['anime_type']
            anime.episodes = animeForm.cleaned_data['episodes']
            anime.rating = animeForm.cleaned_data['rating']
            anime.members = animeForm.cleaned_data['members']
            anime.anime_photo = get_image_url(anime.name)
            anime.save()
            return HttpResponseRedirect("/")
    
    return render(request, 'animes/addanime.html', {'form': animeForm})

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "animes/addcsv.html", data)
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_csv"))
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("upload_csv"))
        csv_file.seek(0)
        reader = csv.DictReader(io.StringIO(csv_file.read().decode('utf-8')),)

        for line in reader:             
            anime = Anime()
            anime.anime_id = line['anime_id']
            anime.name = line['name']
            anime.genre = line['genre']
            anime.anime_type = line['type']
            
            if line['episodes'] == 'Unknown':
                anime.episodes = 0
            elif line['episodes']:
                anime.episodes = line['episodes']
            else:
                anime.episodes = 0
           
            if line['rating'] == 'Unknown':
                anime.rating = 0.0
            elif line['rating']:
                anime.rating = float(line['rating'])
            else:
                anime.rating = 0.0

            if line['members']:
                anime.members = float(line['members'])
            else:
                anime.members = 0
            
            anime.anime_photo = get_image_url(anime.name)
            anime.save()
 
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
 
    return HttpResponseRedirect(reverse("upload_csv"))

def view_animedetails(request, pk):
    try:
        anime_id = Anime.objects.filter(pk=pk).values()
    except Anime.DoesNotExist:
        raise Http404("Anime does not exist")
    
    return render(
        request,
        'animes/listanimedetails.html',
        context={'animes':anime_id,}
    )

#Register a user to be authenticate
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                raise forms.ValidationError('A username with that email or password already exists')

    else:
        form = RegistrationForm()

    return render(request, 'OtakuOrganiserApp/register.html', {'form' : form})

def logout_site(request):
    logout(request)
    return render(request, 'registration/logout.html', 
              {'request': request})

def update(request, anime_id):
    anime = Anime.objects.get(pk = anime_id)
    animeForm = EditAnimeForm(instance = anime)

    if request.method == 'POST':
        animeForm = EditAnimeForm(request.POST, instance = anime)
        if animeForm.is_valid():
            anime.name = animeForm.cleaned_data['name']
            anime.genre= animeForm.cleaned_data['genre']
            anime.anime_type = animeForm.cleaned_data['anime_type']
            anime.episodes = animeForm.cleaned_data['episodes']
            anime.rating = animeForm.cleaned_data['rating']
            anime.members = animeForm.cleaned_data['members']
            anime.save()
            return HttpResponseRedirect("/")
            #return HttpResponse('updated')
        else:
            animeForm = EditAnimeForm()

    return render (request, 'animes/updateanime.html', {'form': animeForm})

def delete(request, pk):
    anime = Anime.objects.get(pk=pk)
    anime.delete()
    return HttpResponseRedirect("/")

def full_anime_listing(request):
    paginator = Paginator(Anime.objects.all(), 30)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        animes = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        animes = paginator.get_page(1)

    return render(request, 'animes/listanime.html', {
        'animes': animes
    })

# search

def search(request):
    query = request.GET.get('anime')
    try:
        results = Anime.objects.get(name=query)
    except Anime.DoesNotExist:
        results = None

    return render(request, 'animes/results.html', {"results": results,})

#Scraping the web and pbtaing images for each anime
def get_soup(url, header):
    return BeautifulSoup(urlopen(Request(url, headers=header)), 'html.parser')


def get_image_url(anime_name):
    anime_name = anime_name.split()
    anime_name = '+'.join(anime_name)
    url = "https://www.google.co.in/search?q=" + anime_name + "&source=lnms&tbm=isch"

    try:
        soup = get_soup(url, {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"})
        a = soup.find("div", {"class": "rg_meta"})
        link = json.loads(a.text)["ou"]
        if len(link) > 1000:
            return "http://i.imgur.com/yEJXUfK.jpg"
        else:
            return json.loads(a.text)["ou"]
    except:
        return "http://i.imgur.com/yEJXUfK.jpg"

def error404(request):
    return render(request, 'animes/404.html', 
              {'request': request})