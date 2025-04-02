from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    RecommendationListView,
)
from . import views

urlpatterns = [
    path('', RecommendationListView.as_view(), name='reader-home'),
    path('add_recommendation/<str:book_id>', views.create_recommendation, name='create_recommendation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)