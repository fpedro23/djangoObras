# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('obras', '0002_auto_20150921_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obra',
            name='municipio',
            field=models.ForeignKey(to='obras.Municipio'),
            preserve_default=True,
        ),
    ]
