from django.urls import path
from . import views

urlpatterns = [
    path('book/<str:olid>/want_to_read/', views.want_to_read, name='want_to_read'),
    path('book/<str:olid>/am_reading/', views.am_reading, name='am_reading'),
    path('book/<str:olid>/have_read/', views.have_read, name='have_read'),
    path('my_lists/', views.reading_list, name='my_lists'),
    path('add_journal_entry/<str:book_id>', views.add_journal_entry, name='add_journal_entry'),
    path('view_journal_entry/<str:book_id>', views.view_journal_entry, name='view_journal_entry'),
]