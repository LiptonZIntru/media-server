from django.contrib import messages
from django.http import FileResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from app.models import User, FilmViewed, Film
from app.decorators import login_required, admin
import moviepy
from moviepy.editor import VideoFileClip
import datetime
import os
import requests
from bs4 import BeautifulSoup

# Create your views here.

file_path = 'app/static/uploaded_films/'
ALLOWED_EXTENSIONS = ['.mp4']  # '.mkv', '.avi'


@require_http_methods(['GET', 'POST'])
@admin
def edit(request, id):
    if request.method == "GET":
        film = Film.objects.get(id=id)
        return render(request, 'films/edit.html', {
            'film': film,
        })
    else:
        Film.objects.filter(id=id).update(
            name=request.POST.get('name'),
            csfd_link=request.POST.get('csfd_link'),
            description=request.POST.get('description'),
        )
        messages.success(request, 'Admin: Film successfully edited')
        return redirect('films')


@admin
def delete(request, id):
    film = Film.objects.filter(id=id)
    os.remove(file_path + film.first().film_url)
    film.delete()
    messages.success(request, 'Admin: Film deleted')
    return redirect('films')
