# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 20:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
