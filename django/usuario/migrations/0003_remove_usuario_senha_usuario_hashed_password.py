# Generated by Django 4.1.3 on 2022-11-10 17:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_alter_usuario_senha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='senha',
        ),
        migrations.AddField(
            model_name='usuario',
            name='hashed_password',
            field=models.CharField(default=None, max_length=100, validators=[django.core.validators.MinLengthValidator(8)], verbose_name='Senha'),
        ),
    ]
