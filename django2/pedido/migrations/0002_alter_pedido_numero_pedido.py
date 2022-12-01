# Generated by Django 4.1.3 on 2022-11-30 16:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='numero_pedido',
            field=models.CharField(default=uuid.uuid4, max_length=100, primary_key=True, serialize=False, verbose_name='Número do pedido'),
        ),
    ]