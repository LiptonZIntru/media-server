from django.contrib import messages
from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from app.models import User, FilmViewed, Film
from app.decorators import login_required
import moviepy
from moviepy.editor import VideoFileClip
import datetime

# Create your views here.

file_path = 'films/'

@login_required
def index(request):
    films = Film.objects.all()
    for film in films:
        film.duration = datetime.timedelta(seconds=int(film.duration))
    return render(request, 'films/index.html',
                  {
                      'films': films,
                  })


@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'films/create.html')
    elif request.method == "POST":
        if not request.FILES.get('file'):
            messages.error(request, 'Vyberte prosím soubor')
            return HttpResponseBadRequest()
            # return redirect('create')

        file = request.FILES['file']

        if not file.name.endswith('.mp4'):
            messages.error(request, 'Soubor není video ve formátu mp4')
            return HttpResponseBadRequest()
            # return redirect('create')

        film_url = file_path + file.name  # request.POST['name']
        f = open(film_url, 'wb+')
        for chunk in file.chunks():
            f.write(chunk)
        Film.objects.create(
            name=request.POST['name'],
            duration=int(VideoFileClip(film_url).duration),
            description=request.POST.get('description'),
            csfd_link=request.POST['csfd_link'],
            author=request.user,
            film_url=film_url
        )
        messages.success(request, 'Film byl přidán')
        return redirect('films')


@login_required
def show(request, id):
    film = Film.objects.filter(id=id)
    film.duration = datetime.timedelta(seconds=int(film.duration))
    return render(request, 'films/show.html',
                  {
                      'film': film,
                  })


@login_required
def edit(request, id):
    if request.method == 'GET':
        film = Film.objects.filter(id=id)[0]
        return render(request, 'films/edit.html',
                      {
                          'film': film,
                      })
    elif request.method == "POST":
        # TODO
        messages.success(request, 'Film byl editován')
        return redirect('films')


@login_required
def film(request, id):
    film_url = Film.objects.filter(id=id)[0].film_url
    return FileResponse(open(film_url, 'rb'))


@login_required
def upload_success(request):
    messages.success(request, 'Film byl přidán')
    return redirect('films')
