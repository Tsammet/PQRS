# Generated by Django 3.2.5 on 2022-04-26 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pqrs', '0007_alter_prqs_cc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prqs',
            name='cc',
            field=models.ForeignKey(max_length=10, on_delete=django.db.models.deletion.CASCADE, to='pqrs.usuario'),
        ),
    ]
