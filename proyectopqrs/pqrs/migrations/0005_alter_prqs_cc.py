# Generated by Django 3.2.5 on 2022-04-22 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqrs', '0004_prqs_estado_pqrs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prqs',
            name='cc',
            field=models.IntegerField(max_length=10),
        ),
    ]
