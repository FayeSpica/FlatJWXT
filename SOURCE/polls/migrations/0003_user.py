# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('polls', '0002_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Uname', models.CharField(max_length=18, unique=True)),
                ('Uemail', models.CharField(max_length=24, unique=True)),
                ('Ufname', models.CharField(max_length=10)),
                ('Ulname', models.CharField(max_length=10)),
                ('UDepartment', models.CharField(max_length=30)),
                ('Upassword', models.CharField(max_length=18)),
            ],
        ),
    ]