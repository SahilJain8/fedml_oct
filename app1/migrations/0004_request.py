# Generated by Django 4.1 on 2023-04-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_hr_managers_rewards_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resever_name', models.CharField(max_length=25)),
                ('senders_name', models.CharField(max_length=25)),
                ('reason', models.CharField(max_length=25)),
                ('points', models.IntegerField()),
            ],
        ),
    ]