# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 19:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seesaw', '0012_auto_20170805_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='create_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
