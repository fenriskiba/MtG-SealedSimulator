# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cardlist', '0004_set_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='rarity',
            field=models.CharField(default='common', max_length=200),
            preserve_default=False,
        ),
    ]
