# Generated by Django 4.0.5 on 2022-07-12 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PrimeraEntregaFinalApp', '0008_foro_remove_post_author_delete_comment_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
