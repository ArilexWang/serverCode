# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 06:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seesaw', '0018_auto_20170806_0507'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seesaw.group'),
        ),
    ]