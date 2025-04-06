from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Book, Recommendation, RecommendationLike

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django import forms
from .forms import RecommendationCreateForm

User = get_user_model()

class RecommendationListView(ListView):
    model = Recommendation
    template_name = 'recommendations/home.html'
    context_object_name = 'recommendations'
    ordering = ['-timestamp']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recommendations = self.get_queryset()
        user_likes = RecommendationLike.objects.filter(user=self.request.user).values_list('recommendation_id', flat=True)
        context['user_likes'] = user_likes  # Pass the IDs of liked recommendations
        return context

@login_required
def create_recommendation(request, *args, **kwargs):
    book = get_object_or_404(Book, id=kwargs['book_id'])

    if request.method == 'POST':
        form = RecommendationCreateForm(request.POST)

        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.book = book
            recommendation.user = request.user
            recommendation.save()
            return redirect(reverse('reader-home'))

    else:
        form = RecommendationCreateForm()
    return render(request, 'recommendations/recommendation_form.html', {'form': form, 'book': book})

class RecommendationDetailView(DetailView):
    model = Recommendation
    template_name = 'recommendations/recommendation_detail.html'
    context_object_name = 'recommendation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recommendation = self.get_object()
        # Check if the current user has liked the recommendation
        context['user_has_liked'] = RecommendationLike.objects.filter(
            user=self.request.user, recommendation=recommendation
        ).exists()
        return context

@login_required
def like_recommendation(request, pk):
    recommendation = get_object_or_404(Recommendation, pk=pk)
    like, created = RecommendationLike.objects.get_or_create(user=request.user, recommendation=recommendation)

    if not created:
        # If the like already exists, remove it (unlike)
        like.delete()

    # Count the total likes for the recommendation
    likes_count = RecommendationLike.objects.filter(recommendation=recommendation).count()

    return JsonResponse({'likes_count': likes_count})