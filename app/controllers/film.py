from django.contrib import messages
from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from app.models import User, FilmViewed, Film
from app.decorators import login_required
import moviepy
from moviepy.editor import VideoFileClip
import datetime
import os

# Create your views here.

file_path = 'app/static/uploaded_films/'
ALLOWED_EXTENSIONS = ['.mp4']  # '.mkv', '.avi'

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
        # validation
        if not request.FILES.get('file'):
            messages.error(request, 'Vyberte prosím soubor')
            return HttpResponseBadRequest()
            # return redirect('create')

        file = request.FILES['file']

        file_extension = ''
        for i in ALLOWED_EXTENSIONS:
            if file.name.endswith(i):
                file_extension = i
        if file_extension == '':
            messages.error(request, 'Formát není podporován')
            return HttpResponseBadRequest()

        if request.POST.get('csfd_link'):
            if request.POST.get('csfd_link').find('https://www.csfd.cz/') == -1:
                messages.error(request, 'Odkaz není na csfd!')
                return HttpResponseBadRequest()

        # end validation
        try:
            file_name = str(Film.objects.last().id + 1)
        except:
            file_name = '1'

        film_url = file_name + file_extension  # request.POST['name']
        f = open(file_path + film_url, 'wb+')
        for chunk in file.chunks():
            f.write(chunk)
        Film.objects.create(
            name=request.POST['name'],
            duration=int(VideoFileClip(file_path + film_url).duration),
            description=request.POST.get('description'),
            csfd_link=request.POST['csfd_link'],
            author=request.user,
            film_url=film_url,
            extension=file_extension,
            size=os.stat(file_path + film_url).st_size
        )
        messages.success(request, 'Film byl přidán')
        return redirect('films')


@login_required
def show(request, id):
    film = Film.objects.filter(id=id)[0]
    film.duration = datetime.timedelta(seconds=int(film.duration))
    film.film_url = "uploaded_films/" + film.film_url
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
    film_url = file_path + Film.objects.filter(id=id)[0].film_url
    return FileResponse(open(film_url, 'rb'))


@login_required
def upload_success(request):
    messages.success(request, 'Film byl přidán')
    return redirect('films')
