# Generated by Django 4.1.3 on 2022-11-11 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_remove_usuario_senha_usuario_hashed_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='sobrenome',
            field=models.CharField(default=None, max_length=100, verbose_name='Sobrenome'),
        ),
    ]
