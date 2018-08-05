# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-25 00:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0005_auto_20180325_0946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workplan',
            name='works',
        ),
        migrations.AddField(
            model_name='workplan',
            name='work',
            field=models.ManyToManyField(help_text='Work to execture in this work plan. Required.', through='work.PracticalWork', to='work.Work'),
        ),
        migrations.AlterField(
            model_name='workplan',
            name='assigned_section',
            field=models.ManyToManyField(blank=True, help_text='Section(s) to assign this work plan.If no team or section is assigned, default of each work will be used.', to='members.Section'),
        ),
        migrations.AlterField(
            model_name='workplan',
            name='assigned_team',
            field=models.ManyToManyField(blank=True, help_text='Team(s) to assign this work plan. If no team or section is assigned, default of each work will be used.', to='members.Team'),
        ),
        migrations.AlterField(
            model_name='workplan',
            name='workplaces',
            field=models.ManyToManyField(blank=True, help_text='Workplace(s) for this work plan.If no workplace is assigned, default of each work will be used.', to='work.Workplace'),
        ),
    ]