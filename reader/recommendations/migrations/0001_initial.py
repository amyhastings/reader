# Generated by Django 4.2.16 on 2025-03-25 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journal', '0005_alter_book_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommend_text', models.TextField()),
                ('recommend_who', models.TextField(blank=True)),
                ('recommend_favourite_part', models.TextField(blank=True)),
                ('recommend_why', models.TextField(blank=True)),
                ('upvotes', models.CharField(max_length=100)),
                ('downvotes', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendation', to='journal.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
