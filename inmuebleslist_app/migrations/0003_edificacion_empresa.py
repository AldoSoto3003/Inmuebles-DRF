# Generated by Django 4.2.3 on 2023-07-14 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebleslist_app', '0002_edificacion_empresa_delete_inmueble'),
    ]

    operations = [
        migrations.AddField(
            model_name='edificacion',
            name='empresa',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Edificacion', to='inmuebleslist_app.empresa'),
            preserve_default=False,
        ),
    ]
