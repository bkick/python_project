# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-25 23:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='patients',
            new_name='Patient',
        ),
    ]
