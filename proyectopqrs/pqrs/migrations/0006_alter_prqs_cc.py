# Generated by Django 3.2.5 on 2022-04-25 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pqrs', '0005_alter_prqs_cc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prqs',
            name='cc',
            field=models.ForeignKey(max_length=10, on_delete=django.db.models.deletion.CASCADE, to='pqrs.usuario'),
        ),
    ]
