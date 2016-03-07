# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20160304_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='text_coords',
            field=models.CommaSeparatedIntegerField(help_text='Area where the label should be displayed (defaults to room coordinates)<br>Please use the following format: <em>x1,y1,x2,y2</em>. <b>Rectangle only!</b>', max_length=50, null=True, verbose_name='Text area coordinates', blank=True),
        ),
    ]
