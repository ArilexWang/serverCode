# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 00:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seesaw', '0015_section_homework_ddl'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='create_time',
            field=models.CharField(default='', max_length=64),
        ),
    ]
