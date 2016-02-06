# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-12 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0004_course_qp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.CharField(max_length=300, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='calc.Session'),
            preserve_default=False,
        ),
    ]
