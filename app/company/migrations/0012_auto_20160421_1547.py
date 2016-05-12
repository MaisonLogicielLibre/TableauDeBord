# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('founder', '0002_auto_20150610_1511'),
        ('company', '0011_company_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='payment_method',
            field=models.CharField(blank=True, max_length=3, verbose_name='Payment method', choices=[(b'CHQ', b'Cheque'), (b'PPA', b'PPA')]),
        ),
        migrations.AddField(
            model_name='company',
            name='person_in_charge',
            field=models.ForeignKey(related_name='in_charge_of', verbose_name='Person in charge', blank=True, to='founder.Founder', null=True),
        ),
    ]
