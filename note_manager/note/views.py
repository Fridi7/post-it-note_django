from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.template.context_processors import csrf

from .forms import PostForm
from .models import Post


#  наверно было бы классно еще сделать список опубликованных заметок


def post_create(request):
    if not request.user.is_authenticated:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Заметка успешно создана")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    if instance.user == request.user:
        # проверка на то, доступна ли заметка пользователю (если он ее не создавал, то нельзя показывать)
        context = {
            "title": instance.title,
            "instance": instance,
        }
        return render(request, "post_detail.html", context)
    else:
        raise Http404


def post_list(request):
    if not request.user.is_active:
        return render(request, "post_list.html")
    else:
        context = {}
        # Количество посещений этого представления, полученное из переменной сессии
        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits + 1

        context.update(csrf(request))
        fname = request.POST.get('filter')
        sname = request.POST.get('sort')
        query = request.POST.get('query')
        queryset_list = Post.objects.filter(user=request.user)

        catlist = []
        datelist = []
        for obj in queryset_list:
            if obj.category not in catlist:
                catlist.append(obj.category)
        for obj in queryset_list:
            if obj.created not in datelist:
                datelist.append(obj.created)

        if fname:
            if fname == "all":
                queryset_list = queryset_list.all()
            elif fname == "favourite":
                queryset_list = queryset_list.filter(favourite=True)
            elif fname[0] == "c":
                queryset_list = queryset_list.filter(category=fname[1:])
            else:
                queryset_list = queryset_list.filter(created=fname)
        if query:
            queryset_list = queryset_list.filter(Q(title__icontains=query) |
                                                 Q(content__icontains=query)
                                                 ).distinct()
        if sname:
            queryset_list = queryset_list.order_by(sname)

        paginator = Paginator(queryset_list, 10)
        page_request_var = 'page'

        page = request.POST.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        context = {
            "query": query,
            "cat_list": catlist,
            "date_list": datelist,
            "object_list": queryset,
            "sort": sname,
            "filter": fname,
            "page_request_var": page_request_var,
            'num_visits': num_visits
        }
        return render(request, "post_list.html", context)


def post_update(request, id=None):
    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,
                    request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Заметка успешно сохранена")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Заметка успешно удалена")
    return redirect("note:list")


def filter_list(request):
    context = {}
    context.update(csrf(request))
    fname = request.POST.get('filter')
    sname = request.POST.get('sort')
    query = request.POST.get('query')
    queryset_list = Post.objects.filter(user=request.user)

    if fname:
        if fname == "all":
            queryset_list = queryset_list.all()
        elif fname == "favourite":
            queryset_list = queryset_list.filter(favourite=True)
        elif fname[0] == "c":
            queryset_list = queryset_list.filter(category=fname[1:])
        else:
            queryset_list = queryset_list.filter(created=fname)
    if query:
        queryset_list = queryset_list.filter(Q(title__icontains=query) |
                                             Q(content__icontains=query)
                                             ).distinct()
    if sname:
        queryset_list = queryset_list.order_by(sname)

    paginator = Paginator(queryset_list, 10)
    page_request_var = 'page'

    page = request.POST.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "page_request_var": page_request_var
    }
    return render(request, "filter_list.html", context)


def post_publish(request, unique_id):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, unique_id=unique_id)
    if instance.uuid_boolean == 0:
        instance.uuid_boolean = 1
        instance.save()
        messages.success(request, "Заметка успешно опубликована")
    context = {
        "instance": instance
    }
    template = loader.get_template('note_static.html')
    return HttpResponse(template.render(context, request))


def publish_delete(request, id=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.uuid_boolean = 0
    instance.save()
    messages.success(request, "Публикация успешно удалена")
    return HttpResponseRedirect(instance.get_absolute_url())
