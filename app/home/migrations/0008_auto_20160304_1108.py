# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20160229_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='company',
            field=models.ForeignKey(related_name='rentals', verbose_name='Company', to='company.Company'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='room',
            field=models.ForeignKey(related_name='rentals', verbose_name='Room', to='home.Room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='coords',
            field=models.CommaSeparatedIntegerField(help_text='For a rectangle, please use the following format: <em>x1,y1,x2,y2</em>.<br>For a polygon, please use the following format: <em>x1,y1,...,xn,yn</em>.', max_length=2000, verbose_name='Coordinates'),
        ),
        migrations.AlterField(
            model_name='room',
            name='static_label',
            field=models.CharField(help_text='<b>Warning:</b> Will be overwritten by rental owner, if any.', max_length=100, verbose_name='Label', blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='text_coords',
            field=models.CommaSeparatedIntegerField(help_text='Area where the label should be displayed (defaults to room coordinates)<br>Please use the following format: <em>x1,y1,x2,y2</em>. <b>Rectangle only!</b>', max_length=50, null=True, verbose_name='Text area coordinates'),
        ),
    ]
