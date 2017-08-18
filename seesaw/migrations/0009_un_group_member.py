# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 00:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seesaw', '0008_group_group_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='un_group_member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seesaw.course')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seesaw.student')),
            ],
        ),
    ]
