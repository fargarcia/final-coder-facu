# Generated by Django 4.0.5 on 2022-07-12 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PrimeraEntregaFinalApp', '0009_comentario'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comentario',
            options={},
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='active',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='body',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='name',
        ),
        migrations.AddField(
            model_name='comentario',
            name='contenido',
            field=models.CharField(default='caca', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comentario',
            name='nombre',
            field=models.CharField(default='caca', max_length=30),
            preserve_default=False,
        ),
    ]
