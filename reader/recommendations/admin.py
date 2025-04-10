from django.contrib import admin
from .models import Recommendation, RecommendationLike

# Show Recommentaion and RecommendationLike in Django admin
admin.site.register(Recommendation)
admin.site.register(RecommendationLike)