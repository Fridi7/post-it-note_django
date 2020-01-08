import uuid, logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Post
from django.contrib import messages, auth
from .forms import PostForm
from django.template.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template import loader

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


def post_detail(request, id=None): ###############, id=None
    instance = get_object_or_404(Post, id=id)
    #instance = get_object_or_404(Post, id=request.POST.get('id', ''))
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    if not request.user.is_active:
        return render(request, "post_list.html")  # need to fixed
    else:
        context = {}
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
            "page_request_var": page_request_var
        }
        return render(request, "post_list.html", context)


def post_update(request, id=None):
    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Post, id=id)

    messages.success(request, str(instance.get_absolute_url()))
    messages.success(request, str(str(instance) + '-instance'))
    form = PostForm(request.POST or None,
                    request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Заметка успешно сохранена")
        link = 'http://127.0.0.1:8000'+str(instance.get_absolute_url())
        messages.success(request, str(link))
        return HttpResponseRedirect(instance.get_absolute_url())
        # return HttpResponseRedirect(uuid.uuid3(uuid.NAMESPACE_URL, str(link)))


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
    # return render_to_response("filter_list.html", context)
    return render("filter_list.html", context)


def post_publish(request, unique_id):
    if not request.user.is_authenticated:
        raise Http404
    messages.success(request, 'вход в функцию p')
    instance = get_object_or_404(Post, unique_id=unique_id)
    messages.success(request, str(instance.get_uuid_url()))
    messages.success(request, str(str(instance) + '-instance'))

    # form = PostForm(request.POST or None,
    #                 request.FILES or None, instance=instance)
    if instance.uuid_boolean == 0:
        instance.uuid_boolean = 1
        instance.save()
        messages.success(request, "поменяли бул")
    #instance = form.save(commit=False)

    messages.success(request, str(str(instance.uuid_boolean) + '-bool'))
    messages.success(request, "Заметка успешно опубликована")
    context = {
        "instance": instance
    }
    template = loader.get_template('note_static.html')
    return HttpResponse(template.render(context, request))


def publish_delete(request, id=None):
    if not request.user.is_authenticated:
        raise Http404
    messages.success(request, 'вход в функцию d')
    instance = get_object_or_404(Post, id=id)
    messages.success(request, str(str(instance) + '-instance'))

    instance.uuid_boolean = 0
    instance.save()
    messages.success(request, "Публикация успешно удалена")
    return HttpResponseRedirect(instance.get_absolute_url())

#
# def post_publish(request, unique_id):
#     if not request.user.is_authenticated:
#         raise Http404
#     messages.success(request, 'вход в функцию')
#     instance = get_object_or_404(Post, unique_id=unique_id)
#     messages.success(request, str(instance.get_uuid_url()))
#     messages.success(request, str(str(instance) + '-instance'))
#
#     form = PostForm(request.POST or None,
#                     request.FILES or None, instance=instance)
#     # if form.is_valid(): #с if not можно псмотерть работу
#     #     instance.uuid_boolean = 1
#     #     instance = form.save(commit=False)
#     #     instance.save()
#     #     messages.success(request, "Заметка успешно опубликована")
#     #     messages.success(request, str(str(instance.uuid_boolean) + '-instance'))
#     #     # messages.success(request, "Successfully published on link: " + str(instance) + str(test))
#     #     return HttpResponseRedirect(instance.get_uuid_url())
#     if instance.uuid_boolean == 1:
#         instance.uuid_boolean = 0
#         instance = form.save(commit=False)
#         instance.save()
#         messages.success(request, "Публикация успешно удалена")
#         #return render(request, "post_detail.html", context)
#         return HttpResponseRedirect(instance.get_absolute_url())
#
#     elif instance.uuid_boolean == 0:
#         instance.uuid_boolean = 1
#         messages.success(request, "Заметка успешно опубликована")
#         instance = form.save(commit=False)
#         instance.save()
#
#         messages.success(request, str(str(instance.uuid_boolean) + '-bool'))
#
#         context = {
#             "instance": instance
#         }
#         # return render(request, "post_form.html", context)
#         template = loader.get_template('note_static.html')
#         return HttpResponse(template.render(context, request))
#
