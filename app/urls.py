"""video_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from .controllers import auth, film, home

urlpatterns = [
    path('', home.index, name='index'),
    path('login/', auth.user_login, name='login'),
    path('register/', auth.user_register, name='register'),
    path('logout/', auth.user_logout),
    path('films/', film.index, name='films'),
    path('films/create/', film.create, name='create'),
    path('films/success/', film.upload_success),
    # path('films/<id>/', film.show),

    path('films/<id>/', film.show),  # temporary

    path('films/<id>/edit', film.edit),

    path('film/<id>/', film.film),

    path('films/<id>/save/', csrf_exempt(film.saveViewed)),
]
