from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Book, Recommendation, RecommendationLike

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django import forms
from .forms import RecommendationCreateForm, RecommendationUpdateForm

User = get_user_model()

# Show all Recommendations
class RecommendationListView(ListView):
    model = Recommendation
    template_name = 'recommendations/home.html'
    context_object_name = 'recommendations'
    ordering = ['-timestamp']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recommendations = self.get_queryset()
        # Get the ids of all of the Recommendations that the current user has liked so we can show them as liked in the UI
        if self.request.user.is_authenticated:
            user_likes = RecommendationLike.objects.filter(user=self.request.user).values_list('recommendation_id', flat=True)
            context['user_likes'] = user_likes
        else:
            context['user_likes'] = []
        return context

# Create a new Recommendation
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

# Show a particular Recommendation
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

# Mark a particular Recommendation as liked by a User (called by js)
@login_required
def like_recommendation(request, pk):
    recommendation = get_object_or_404(Recommendation, pk=pk)
    like, created = RecommendationLike.objects.get_or_create(user=request.user, recommendation=recommendation)

    if not created:
        # If the like already exists, remove it (unlike)
        like.delete()

    # Count the total likes for the recommendation
    likes_count = RecommendationLike.objects.filter(recommendation=recommendation).count()

    return JsonResponse({'likes_count': likes_count}, status=200)

# Show Recommendations for a particular User
class UserRecommendationListView(ListView):
    model = Recommendation
    template_name = 'recommendations/my_recommendations.html'
    context_object_name = 'user_recommendations'
    paginate_by = 5

    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user).order_by('timestamp')

# Update a Recommendation
class RecommendationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Recommendation
    template_name = 'recommendations/update_recommendation_form.html'
    form_class = RecommendationUpdateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        recommendation = get_object_or_404(Recommendation, id=self.kwargs['pk'])
        return reverse_lazy('recommendation_detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        recommendation = self.get_object()
        return self.request.user == recommendation.user

# Delete a Recommendation
class RecommendationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recommendation
    template_name = 'recommendations/recommendation_confirm_delete.html'

    def test_func(self):
        recommendation = self.get_object()
        return self.request.user == recommendation.user
    
    def get_success_url(self):
        return reverse_lazy('all_user_recommendations')

# Generic error handler function
def error(request, *args, **argv):
    return render(request, 'recommendations/error.html', status=404)