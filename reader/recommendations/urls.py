from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    RecommendationListView,
    RecommendationDetailView,
    RecommendationUpdateView,
    RecommendationDeleteView,
    UserRecommendationListView,
)
from . import views

urlpatterns = [
    path('', RecommendationListView.as_view(), name='reader-home'),
    path('add_recommendation/<str:book_id>', views.create_recommendation, name='create_recommendation'),
    path('recommendation/<int:pk>', RecommendationDetailView.as_view(), name='recommendation_detail'),
    path('recommendation/<int:pk>/like/', views.like_recommendation, name='like-recommendation'),
    path('recommendation/<int:pk>/update/', RecommendationUpdateView.as_view(), name='update_recommendation'),
    path('recommendation/delete_recommendation/<int:pk>', RecommendationDeleteView.as_view(), name='delete_recommendation'),
    path('my_recommendations/', UserRecommendationListView.as_view(), name='all_user_recommendations'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)