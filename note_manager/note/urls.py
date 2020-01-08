from django.urls import path, include

from . import views
from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    filter_list,
    post_publish,
    publish_delete,
)

app_name = 'note'
urlpatterns = [
    # url(r'^notes/filters/$', filter_list),
    path('notes/filters/', filter_list),
    path('', post_list, name='list'),
    #url(r'^$', post_list, name='list'),
    path('create/', post_create, name='create'),
    # url(r'^note/create/$', post_create),  # костыль
    # url(r'^(?P<id>[\w]+)$', post_detail, name='detail'),
    path('<int:id>/', post_detail, name='detail'),
    # url(r'^(?P<id>[\w]+)/edit/', post_update, name='update'),
    path('<int:id>/edit/', post_update, name='update'),  # нужно так делать
    path('<int:id>/delete/', post_delete, name='delete'),
    path('<uuid:unique_id>/', post_publish, name='publish'),  #'<uuid:unique_id/publish/>', post_publish, name='publish'
    path('<int:id>/publish_delete', publish_delete, name='publish_delete'),
    # url(r'^(?P<id>[\w]+)/delete/$', post_delete),


]
