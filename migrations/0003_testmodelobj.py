# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-04 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table_foo', '0002_auto_20170504_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModelObj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attr_1', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
