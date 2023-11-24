

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('MOVIES', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dislike_review_users', models.ManyToManyField(related_name='dislike_reviews', to=settings.AUTH_USER_MODEL)),
                ('like_review_users', models.ManyToManyField(related_name='like_reviews', to=settings.AUTH_USER_MODEL)),
                ('super_review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewed', to='COMMUNITY.review')),
                ('write_review_movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='write_movie_review', to='MOVIES.movie')),
                ('write_review_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='write_review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('commented_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_comment', to='COMMUNITY.review')),
                ('like_comment_users', models.ManyToManyField(related_name='like_comments', to=settings.AUTH_USER_MODEL)),
                ('super_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commented', to='COMMUNITY.comment')),
                ('write_comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='write_comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
