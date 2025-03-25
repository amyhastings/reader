from django.urls import path
from . import views
from .views import (
    UserJournalEntryListView,
    JournalEntryUpdateView,
    JournalEntryDeleteView,
)

urlpatterns = [
    path('book/<str:olid>/want_to_read/', views.want_to_read, name='want_to_read'),
    path('book/<str:olid>/am_reading/', views.am_reading, name='am_reading'),
    path('book/<str:olid>/have_read/', views.have_read, name='have_read'),
    path('change_book_status/<int:book_id>/<str:status>/', views.change_book_status, name='change_book_status'),
    path('delete_book_to_user/<int:book_id>/', views.delete_book_to_user, name='delete_book_to_user'),
    path('my_lists/', views.reading_list, name='my_lists'),
    path('add_journal_entry/<str:book_id>', views.create_journal_entry, name='create_journal_entry'),
    path('view_journal_entry/<str:book_id>', views.view_journal_entry, name='view_journal_entry'),
    path('update_journal_entry/<int:pk>', JournalEntryUpdateView.as_view(), name='update_journal_entry'),
    path('delete_journal_entry/<int:pk>', JournalEntryDeleteView.as_view(), name='delete_journal_entry'),
    path('my_journal/', UserJournalEntryListView.as_view(), name='all_journal_entries'),
]