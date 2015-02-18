# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cardlist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sets',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set_name', models.CharField(max_length=200)),
                ('set_abbrev', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='card',
            name='set_name',
        ),
    ]
