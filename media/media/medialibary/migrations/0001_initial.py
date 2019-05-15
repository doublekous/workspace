# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MediaLibrary',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('url', models.CharField(max_length=255, null=True, verbose_name=b'\xe9\x93\xbe\xe6\x8e\xa5', blank=True)),
                ('secondpage', models.CharField(max_length=255, null=True, verbose_name=b'\xe4\xba\x8c\xe7\xba\xa7\xe9\x9d\xa2\xe6\x9d\xbf', blank=True)),
                ('thirdpage', models.CharField(max_length=255, null=True, verbose_name=b'\xe4\xb8\x89\xe7\xba\xa7\xe9\x9d\xa2\xe6\x9d\xbf', blank=True)),
                ('xunxun_nickname', models.CharField(max_length=255, null=True, verbose_name=b'\xe8\xae\xaf\xe8\xae\xaf\xe5\x88\xab\xe7\xa7\xb0', blank=True)),
                ('sousou_nickname', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x90\x9c\xe6\x90\x9c\xe5\x88\xab\xe7\xa7\xb0', blank=True)),
                ('website', models.CharField(max_length=255, null=True, verbose_name=b'\xe7\xbd\x91\xe7\xab\x99', blank=True)),
                ('sitetype', models.CharField(max_length=255, null=True, verbose_name=b'\xe7\xbd\x91\xe7\xab\x99\xe7\xb1\xbb\xe5\x9e\x8b', blank=True)),
                ('regional', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\x9c\xb0\xe5\x9f\x9f', blank=True)),
                ('fetchlevel', models.IntegerField(default=1, verbose_name=b'\xe6\x8a\x93\xe5\x8f\x96\xe7\xad\x89\xe7\xba\xa7', choices=[(1, b'\xe5\x85\xa8\xe9\x83\xa8'), (2, b'\xe9\xab\x98'), (3, b'\xe4\xb8\xad'), (4, b'\xe4\xbd\x8e')])),
                ('yesterdaycapture', models.IntegerField(null=True, verbose_name=b'\xe6\x98\xa8\xe6\x97\xa5\xe6\x8a\x93\xe5\x8f\x96\xe9\x87\x8f')),
                ('is_author', models.IntegerField(default=0, null=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe6\x9c\x89\xe4\xbd\x9c\xe8\x80\x85/\xe4\xba\x92\xe5\x8a\xa8/\xe5\x8e\x9f\xe5\x88\x9b', blank=True, choices=[(1, b'\xe6\x97\xa0'), (2, b'\xe6\x9c\x89\xe4\xbd\x9c\xe8\x80\x85'), (3, b'\xe6\x9c\x89\xe4\xba\x92\xe5\x8a\xa8'), (4, b'\xe6\x9c\x89\xe5\x8e\x9f\xe5\x88\x9b\xe8\xbd\xac\xe8\xbd\xbd')])),
                ('addpaper', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe4\xba\xba', blank=True)),
                ('addtime', models.DateField(auto_now_add=True, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4')),
                ('updatetime', models.DateField(auto_now_add=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('latestfetchtime', models.DateField(auto_now_add=True, verbose_name=b'\xe6\x9c\x80\xe6\x96\xb0\xe6\x8a\x93\xe5\x8f\x96\xe6\x97\xb6\xe9\x97\xb4')),
                ('fetchstatus', models.IntegerField(default=1, verbose_name=b'\xe6\x8a\x93\xe5\x8f\x96\xe7\x8a\xb6\xe6\x80\x81', choices=[(1, b'\xe5\x85\xa8\xe9\x83\xa8'), (2, b'\xe5\xa4\xb1\xe8\xb4\xa5'), (3, b'\xe5\xae\x8c\xe6\x88\x90')])),
                ('is_process', models.IntegerField(verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xa4\x84\xe7\x90\x86', choices=[(1, b'\xe5\x85\xa8\xe9\x83\xa8'), (2, b'\xe6\x9c\xaa\xe5\xa4\x84\xe7\x90\x86'), (3, b'\xe5\xb7\xb2\xe5\xa4\x84\xe7\x90\x86'), (4, b'\xe6\x97\xa0')])),
                ('note', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
                ('date1', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x95\xb0\xe6\x8d\xae\xe4\xb8\x80', blank=True)),
                ('is_xuxu', models.IntegerField(default=1, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xba\x94\xe7\x94\xa8\xe5\x88\xb0\xe8\xae\xaf\xe8\xae\xaf', choices=[(1, b'\xe5\x85\xa8\xe9\x83\xa8'), (2, b'\xe6\x98\xaf'), (3, b'\xe5\x90\xa6')])),
                ('is_sousou', models.IntegerField(default=1, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xba\x94\xe7\x94\xa8\xe5\x88\xb0\xe6\x90\x9c\xe6\x90\x9c', choices=[(1, b'\xe5\x85\xa8\xe9\x83\xa8'), (2, b'\xe6\x98\xaf'), (3, b'\xe5\x90\xa6')])),
                ('many_choice', models.IntegerField(blank=True, null=True, verbose_name=b'\xe9\x93\xbe\xe6\x8e\xa5', choices=[(1, b'\xe9\x93\xbe\xe6\x8e\xa5'), (2, b'\xe7\xbd\x91\xe7\xab\x99'), (3, b'\xe4\xba\x8c\xe7\xba\xa7\xe7\x89\x88\xe9\x9d\xa2'), (4, b'\xe4\xb8\x89\xe7\xba\xa7\xe7\x89\x88\xe9\x9d\xa2'), (5, b'\xe5\x8d\xb1\xe6\x9c\xbaAPP\xe5\x88\xab\xe7\xa7\xb0'), (6, b'\xe6\x90\x9c\xe6\x90\x9c\xe5\x88\xab\xe7\xa7\xb0'), (7, b'\xe7\xbd\x91\xe7\xab\x99\xe7\xb1\xbb\xe5\x9e\x8b'), (8, b'\xe5\x9c\xb0\xe5\x9f\x9f')])),
                ('is_del', models.IntegerField(default=0, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x88\xa0\xe9\x99\xa4', choices=[(1, b'\xe6\x98\xaf'), (0, b'\xe5\x90\xa6')])),
                ('count', models.IntegerField(default=0, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe9\x87\x8f')),
            ],
            options={
                'db_table': 'mx_medialibary',
            },
        ),
    ]
