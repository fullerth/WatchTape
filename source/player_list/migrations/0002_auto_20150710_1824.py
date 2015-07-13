# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player_list', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videotojam',
            name='jam',
            field=models.ForeignKey(to='player_list.Jam', null=True, blank=True),
        ),
    ]
