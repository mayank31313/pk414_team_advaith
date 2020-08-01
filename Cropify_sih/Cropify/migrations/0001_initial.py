# Generated by Django 3.0.4 on 2020-07-24 15:22

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=10, unique=True)),
                ('pincode', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
