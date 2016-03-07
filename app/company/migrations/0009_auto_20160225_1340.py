# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_auto_20150918_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='companyStatus',
            field=models.ForeignKey(related_name='companies', verbose_name='Status', to='company.CompanyStatus'),
        ),
    ]
