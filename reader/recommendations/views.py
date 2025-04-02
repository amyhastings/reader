from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Book, Recommendation

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