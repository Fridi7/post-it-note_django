from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.template.context_processors import csrf


def user_create(request):
    context = {}
    context.update(csrf(request))
    if request.POST:
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = User.objects.create_user(username, email, password)
        if user.is_active:
            user.save()
            return HttpResponseRedirect("/note")
        else:
            context["creating_error"] = "Не удалось создать пользователя"
            return render(request, "user-create.html", context)
    else:
        return render(request, "user-create.html", context)


def login(request):
    context = {}
    context.update(csrf(request))
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect("/note")
        else:
            context["login_error"] = "Пользователь не найден"
            return render(request, "login.html", context)
    else:
        return render(request, "login.html", context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/note")
