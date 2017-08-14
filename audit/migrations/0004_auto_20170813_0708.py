# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 07:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0003_sessionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditlog',
            name='cmd',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auditlog',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auditlog',
            name='session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='audit.SessionLog'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sessionlog',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
