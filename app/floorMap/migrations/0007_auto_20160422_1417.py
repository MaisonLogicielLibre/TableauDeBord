# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('floorMap', '0006_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='taxes_tps',
            field=models.DecimalField(default=0, verbose_name='TPS %', max_digits=5, decimal_places=3),
        ),
        migrations.AddField(
            model_name='settings',
            name='taxes_tvq',
            field=models.DecimalField(default=0, verbose_name='TVQ %', max_digits=5, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='settings',
            name='default_annual_rental_rate',
            field=models.DecimalField(default=0, help_text='Per sq. ft.', verbose_name='Default annual rental rate', max_digits=5, decimal_places=2),
        ),
    ]
