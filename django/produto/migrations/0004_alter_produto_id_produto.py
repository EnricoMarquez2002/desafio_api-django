# Generated by Django 4.1.3 on 2022-11-16 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_alter_produto_id_produto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='id_produto',
            field=models.CharField(default=None, editable=False, max_length=100, primary_key=True, serialize=False, unique=True, verbose_name='Id Produto'),
        ),
    ]
