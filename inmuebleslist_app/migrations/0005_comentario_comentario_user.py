# Generated by Django 4.2.3 on 2023-07-24 17:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inmuebleslist_app', '0004_alter_edificacion_empresa_comentario'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='comentario_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
