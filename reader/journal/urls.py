from django.urls import path
from . import views

urlpatterns = [
    path('book/<str:olid>/want_to_read/', views.want_to_read, name='want_to_read'),
    path('book/<str:olid>/am_reading/', views.am_reading, name='am_reading'),
    path('book/<str:olid>/have_read/', views.have_read, name='have_read'),
]