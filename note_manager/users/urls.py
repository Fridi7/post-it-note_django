from django.urls import path

from .views import (
    user_create,
    login,
    logout,
)

app_name = 'users'
urlpatterns = [
    path('user-create/', user_create, name='user_create'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
