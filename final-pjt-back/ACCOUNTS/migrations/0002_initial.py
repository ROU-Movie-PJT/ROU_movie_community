

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('MOVIES', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('ACCOUNTS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hate_genres',
            field=models.ManyToManyField(blank=True, related_name='hate_users', to='MOVIES.genre'),
        ),
        migrations.AddField(
            model_name='user',
            name='like_genres',
            field=models.ManyToManyField(blank=True, related_name='like_users', to='MOVIES.genre'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
