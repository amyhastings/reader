from django.contrib import admin
from .models import Recommendation, RecommendationLike

admin.site.register(Recommendation)
admin.site.register(RecommendationLike)