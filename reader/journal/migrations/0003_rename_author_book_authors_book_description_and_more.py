# Generated by Django 4.2.16 on 2025-03-18 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_book_cover'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='author',
            new_name='authors',
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.CharField(default='', max_length=10000),
        ),
        migrations.AddField(
            model_name='book',
            name='edition_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='first_publish_year',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='subjects',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
