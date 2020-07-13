from django.contrib import messages
from django.shortcuts import redirect


def login_required(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            messages.error(request, 'Pro tuto akci je potřeba se přihlásit')
            return redirect('login')
    return wrapper_func
