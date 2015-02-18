# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cardlist', '0002_auto_20150218_1656'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sets',
            new_name='Set',
        ),
    ]
