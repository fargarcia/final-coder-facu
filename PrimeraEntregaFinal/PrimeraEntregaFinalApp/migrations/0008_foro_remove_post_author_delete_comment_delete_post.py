# Generated by Django 4.0.5 on 2022-07-12 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PrimeraEntregaFinalApp', '0007_post_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Foro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentarios', models.CharField(max_length=300)),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
