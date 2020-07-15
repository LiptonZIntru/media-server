from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from app.decorators import login_required


# Create your views here.
from app.models import User


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    elif request.method == "GET":
        return render(request, 'auth/index.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            messages.success(request, 'Vítej ' + user.username + '!')
            return redirect('index')
        else:
            messages.error(request, 'Špatné údaje!')
            return redirect('login')


@require_http_methods(["GET", "POST"])
def user_register(request):
    if request.user.is_authenticated:
        return redirect('index')
    elif request.method == "GET":
        return render(request, 'auth/register.html')
    else:
        try:
            User.objects.create_user(
                request.POST['username'],
                request.POST['password'],
            )
            messages.success(request, 'Registrace úspěšná!')
            return redirect('login')
        except:
            messages.error(request, 'Neznámá chyba')
            return redirect('register')



@login_required
@require_http_methods(["GET"])
def user_logout(request):
    logout(request)
    messages.success(request, 'Byl jsi úspěšně odhlášen')
    return redirect('login')
