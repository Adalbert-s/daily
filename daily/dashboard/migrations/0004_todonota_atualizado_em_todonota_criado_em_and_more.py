# Generated by Django 5.2 on 2025-05-26 05:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_todonota_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='todonota',
            name='atualizado_em',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='todonota',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='todonota',
            name='data',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='todonota',
            name='hora',
            field=models.TimeField(),
        ),
    ]
