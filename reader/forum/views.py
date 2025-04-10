from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django import forms

from .models import Topic, Thread, Post
from .forms import ThreadCreateForm, FirstPostCreateForm, CommentCreateForm

User = get_user_model()

# Show all of the Topics in the forum
class TopicListView(ListView):
    model = Topic
    template_name = 'forum/topic_list.html'
    fields = ['title', 'description']
    context_object_name = 'topics'
    
    def get_context_data(self, *args, **kwargs):
        context = super(TopicListView, self).get_context_data(*args, **kwargs)
        topics = context['topics']
        for topic in topics:
            topic.thread_count = Thread.objects.filter(topic=topic).count()
        return context

# Show all of the Threads in a Topic
class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/thread_list.html'
    fields = ['title', 'author', 'timestamp']
    context_object_name = 'threads'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(ThreadListView, self).get_context_data(*args, **kwargs)
        # Get the topic from the URL params
        context['topic'] = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        threads = context['threads']
        # Work out how many posts are in each Thread so we can show a count
        for thread in threads:
            thread.post_count = Post.objects.filter(thread=thread).count()
        return context

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        return Thread.objects.filter(topic=self.topic).order_by('-timestamp')

# Create a new Thread
@login_required
def create_thread(request):
    if request.method == 'POST':
        # Use two forms here. One to create the Thread and one to create the fist Post.
        t_form = ThreadCreateForm(request.POST)
        p_form = FirstPostCreateForm(request.POST, request.FILES)

        if t_form.is_valid() and p_form.is_valid():
            thread = t_form.save(commit=False)
            thread.author = request.user
            thread.save()
            post = p_form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            return redirect("/forum/topic/%d/thread/%d" % (thread.topic.id, thread.id))
    else:
        t_form = ThreadCreateForm()
        p_form = FirstPostCreateForm()
    return render(request, 'forum/thread_form.html', {'t_form': t_form, 'p_form': p_form})

# Show all Posts in a Thread
class PostListView(ListView):
    model = Post
    template_name = 'forum/thread_post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        # Get the specific Thread and Topic from the URL params
        context['topic'] = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        context['thread'] = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return context

    def get_queryset(self):
        self.thread = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return Post.objects.filter(thread=self.thread).order_by('timestamp')

# Add a Post to a Thread
@login_required
def create_comment(request, *args, **kwargs):
    thread = get_object_or_404(Thread, id=kwargs['thread_id'])

    if request.method == 'POST':
        form = CommentCreateForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            # After creating the Post, send the user back to the Thread
            return redirect(reverse('view-thread', kwargs={'topic_id': post.thread.topic.id, 'thread_id': post.thread.id}))

    else:
        form = CommentCreateForm()
    return render(request, 'forum/post_form.html', {'form': form, 'thread': thread})

# Show all Posts for a given user
class UserPostListView(ListView):
    model = Post
    template_name = 'forum/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user.posts.order_by('-timestamp')

# Update a particular Post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'forum/post_form.html'
    fields = ['content']

    def get_context_data(self, *args, **kwargs):
        context = super(PostUpdateView, self).get_context_data(*args, **kwargs)
        # Get the specific Thread and Topic from the URL params
        context['topic'] = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        context['thread'] = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.thread = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse_lazy('view-thread', kwargs={'topic_id': self.kwargs['topic_id'], 'thread_id': self.kwargs['thread_id']})

# Delete a particular Post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'forum/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostDeleteView, self).get_context_data(*args, **kwargs)
        context['topic'] = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        context['thread'] = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return context
            
    def get_success_url(self):
        return reverse_lazy('view-thread', kwargs={'topic_id': self.kwargs['topic_id'], 'thread_id': self.kwargs['thread_id']})

