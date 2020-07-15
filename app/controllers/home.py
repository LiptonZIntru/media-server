from django.shortcuts import render
from app.decorators import login_required
from app.models import User, FilmViewed, Film, LastViewed


# Create your views here.


@login_required
def index(request):
    films = LastViewed.objects.filter(user=request.user).order_by('id').reverse()
    last_viewed = []
    try:
        last_viewed.append(films[0])
    except:
        pass
    for i in films[1:len(films)]:
        valid = True
        for a in last_viewed:
            if a.film == i.film:
                valid = False
        if valid and len(last_viewed) <= 4:
            last_viewed.append(i)
        if len(last_viewed) >= 4:
            break
    top_films = Film.objects.order_by('watched_seconds').reverse()[:4]
    return render(request, 'home/index.html',
                  {
                      'last_viewed': last_viewed,
                      'top_films': top_films
                  })
