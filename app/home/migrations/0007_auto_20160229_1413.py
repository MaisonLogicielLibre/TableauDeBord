# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20160225_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='companies',
        ),
        migrations.AlterField(
            model_name='rent',
            name='company',
            field=models.ForeignKey(related_name='Rentals', verbose_name='Company', to='company.Company'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='room',
            field=models.ForeignKey(related_name='Rentals', verbose_name='Room', to='home.Room'),
        ),
    ]
