# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('obras', '0003_auto_20150921_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obra',
            name='municipio',
            field=models.ForeignKey(blank=True, to='obras.Municipio', null=True),
            preserve_default=True,
        ),
    ]
