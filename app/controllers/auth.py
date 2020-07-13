from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from app.decorators import login_required


# Create your views here.


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

@login_required
@require_http_methods(["GET"])
def user_logout(request):
    logout(request)
    messages.success(request, 'Byl jsi úspěšně odhlášen')
    return redirect('login')
