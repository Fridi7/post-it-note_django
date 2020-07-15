from django.urls import path

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
    path('notes/filters/', filter_list),
    path('', post_list, name='list'),
    path('create/', post_create, name='create'),
    path('<int:id>/', post_detail, name='detail'),
    path('<int:id>/edit/', post_update, name='update'),
    path('<int:id>/delete/', post_delete, name='delete'),
    path('<uuid:unique_id>/', post_publish, name='publish'),
    path('<int:id>/publish_delete', publish_delete, name='publish_delete'),
]

