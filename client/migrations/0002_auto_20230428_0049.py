# Generated by Django 3.2.18 on 2023-04-28 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client_model_weights',
            name='model_weights',
        ),
        migrations.AddField(
            model_name='client_model_weights',
            name='weights',
            field=models.BinaryField(default=0),
            preserve_default=False,
        ),
    ]
