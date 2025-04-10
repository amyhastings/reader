from django.contrib import admin
from .models import Topic, Thread, Post

# Show Topic, Thread, and Post in Django admin
admin.site.register(Topic)
admin.site.register(Thread)
admin.site.register(Post)