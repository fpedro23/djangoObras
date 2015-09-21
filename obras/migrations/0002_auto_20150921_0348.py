# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('obras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obra',
            name='municipio',
            field=models.ForeignKey(default=33, to='obras.Municipio'),
            preserve_default=True,
        ),
    ]
