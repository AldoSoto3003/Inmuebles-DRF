# Generated by Django 4.2.3 on 2023-07-24 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebleslist_app', '0005_comentario_comentario_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='edificacion',
            name='avg_calificacion',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='edificacion',
            name='number_calificacion',
            field=models.IntegerField(default=0),
        ),
    ]
