# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_auto_20160225_1340'),
        ('home', '0005_floorplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_start', models.DateField(verbose_name='Start date')),
                ('date_end', models.DateField(verbose_name='End date')),
                ('company', models.ForeignKey(verbose_name='Company', to='company.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10, verbose_name='Code', blank=True)),
                ('static_label', models.CharField(max_length=100, verbose_name='Label', blank=True)),
                ('coords', models.CommaSeparatedIntegerField(max_length=2000, verbose_name='Coordinates')),
                ('text_coords', models.CommaSeparatedIntegerField(max_length=50, null=True, verbose_name='Text area coordinates')),
                ('companies', models.ManyToManyField(to='company.Company', verbose_name='Rented by', through='home.Rent')),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.CharField(max_length=b'100', verbose_name='Description', blank=True)),
                ('is_rental', models.BooleanField(default=False, verbose_name='Is rental')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='type',
            field=models.ForeignKey(verbose_name='Type', to='home.RoomType'),
        ),
        migrations.AddField(
            model_name='rent',
            name='room',
            field=models.ForeignKey(verbose_name='Room', to='home.Room'),
        ),
    ]
