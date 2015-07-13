# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import player_list.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bout',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('date', models.DateField(verbose_name='date played', default=datetime.date.today)),
                ('location', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Jam',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('half', models.IntegerField(default=1)),
                ('home_jammer_score', models.IntegerField(default=0)),
                ('away_jammer_score', models.IntegerField(default=0)),
                ('home_pivot_score', models.IntegerField(default=0)),
                ('away_pivot_score', models.IntegerField(default=0)),
                ('home_cumulative_score', models.IntegerField(default=0)),
                ('away_cumulative_score', models.IntegerField(default=0)),
                ('home_star_pass', models.BooleanField(default=False)),
                ('away_star_pass', models.BooleanField(default=False)),
                ('bout', models.ForeignKey(to='player_list.Bout')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('penalty', models.CharField(max_length=2, choices=[('B', 'Back Block'), ('A', 'High Block'), ('L', 'Low Block'), ('E', 'Elbows'), ('F', 'Forearms'), ('H', 'Blocking With Head'), ('M', 'Multi-Player'), ('O', 'Out of Bounds Block/Assist'), ('C', 'Direction of Play'), ('P', 'Out of Play'), ('X', 'Cutting'), ('S', 'Skating out of bounds'), ('I', 'Illegal Procedure'), ('N', 'Insubordination'), ('Z', 'Delay of Game'), ('G', 'Gross Misconduct')])),
                ('jam_called', models.ForeignKey(to='player_list.Jam', related_name='penalty_jam_called')),
                ('jam_released', models.ForeignKey(to='player_list.Jam', related_name='penalty_jam_released')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('number', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerToJam',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('position', models.CharField(max_length=1, choices=[('B', 'Blocker'), ('J', 'Jammer'), ('P', 'Pivot')])),
                ('jam', models.ForeignKey(to='player_list.Jam')),
                ('player', models.ForeignKey(to='player_list.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerToRoster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('captain', models.BooleanField(default=False)),
                ('player', models.ForeignKey(to='player_list.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('players', models.ManyToManyField(through='player_list.PlayerToRoster', to='player_list.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('players', models.ManyToManyField(null=True, to='player_list.Player', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('url', models.URLField(max_length=255)),
                ('source', models.CharField(max_length=200)),
                ('site', models.CharField(max_length=7, choices=[('vimeo', 'http://vimeo.com'), ('youtube', 'http://youtube.com'), ('', 'unknown')])),
                ('player_url', models.CharField(max_length=2000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoToJam',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('start_time', models.CharField(max_length=200, validators=[player_list.models._timecode_validator])),
                ('end_time', models.CharField(max_length=200, validators=[player_list.models._timecode_validator], blank=True)),
                ('timecode_url', models.URLField(max_length=255, blank=True)),
                ('jam', models.ForeignKey(to='player_list.Jam')),
                ('video', models.ForeignKey(null=True, to='player_list.Video', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='roster',
            name='team',
            field=models.ForeignKey(to='player_list.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playertoroster',
            name='roster',
            field=models.ForeignKey(to='player_list.Roster'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='penalty',
            name='player',
            field=models.ForeignKey(to='player_list.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='league',
            name='teams',
            field=models.ForeignKey(to='player_list.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jam',
            name='players',
            field=models.ManyToManyField(through='player_list.PlayerToJam', to='player_list.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jam',
            name='videos',
            field=models.ManyToManyField(through='player_list.VideoToJam', to='player_list.Video'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bout',
            name='away_roster',
            field=models.ForeignKey(null=True, related_name='away_roster', blank=True, to='player_list.Roster'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bout',
            name='home_roster',
            field=models.ForeignKey(null=True, related_name='home_roster', blank=True, to='player_list.Roster'),
            preserve_default=True,
        ),
    ]
