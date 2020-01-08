from django.urls import path

from .views import (
    user_create,
    login,
    logout,
)

app_name = 'users'
urlpatterns = [
    # url(r'^user-create/$', user_create),
    # url(r'^login/$', login),
    # url(r'^logout/$', logout),
    path('user-create/', user_create),
    path('login/', login),
    path('logout/', logout),
]
