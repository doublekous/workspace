# -*- coding: utf-8 -*-
from django.db import models


class MediaLibrary(models.Model):
   # id = models.AutoField(primary=True)

    url = models.CharField(verbose_name="链接", max_length=255, blank=True, null=True)
    secondpage = models.CharField(verbose_name="二级面板", max_length=255, blank=True, null=True)
    thirdpage = models.CharField(verbose_name="三级面板", max_length=255, blank=True, null=True)
    xunxun_nickname = models.CharField(verbose_name="讯讯别称", max_length=255, blank=True, null=True)
    sousou_nickname = models.CharField(verbose_name="搜搜别称", max_length=255, blank=True, null=True)
    website = models.CharField(verbose_name="网站", max_length=255, blank=True, null=True)
    sitetype = models.CharField(verbose_name="网站类型", max_length=255, blank=True, null=True)
    regional = models.CharField(verbose_name="地域", max_length=255, blank=True, null=True)
    fetchlevel = models.IntegerField(verbose_name="抓取等级", choices=((1, '全部'), (2, '高'), (3, '中'), (4, '低')), default=1)
    yesterdaycapture = models.IntegerField(verbose_name="昨日抓取量", null=True)
    author_mode = (
        (1, '无'),
        (2, '有作者'),
        (3, '有互动'),
        (4, '有原创转载'),

    )
    is_author = models.IntegerField(verbose_name="是否有作者/互动/原创",choices=author_mode, default=0, blank=True, null=True)
    addpaper = models.CharField(verbose_name="添加人", max_length=255)
    addtime = models.DateField(verbose_name="添加时间", auto_now_add=True)
    updatetime = models.DateField(verbose_name="修改时间", auto_now_add=True)
    latestfetchtime = models.DateField(verbose_name="最新抓取时间", auto_now_add=True)
    fetchstatus = models.IntegerField(verbose_name="抓取状态", choices=((1, '全部'), (2, '失败'), (3, '完成')),default=1)
    is_process = models.IntegerField(verbose_name="是否处理", choices=((1, '全部'),(2, '未处理'), (3, '已处理'), (4, '无')))
    note = models.CharField(verbose_name="备注", max_length=255, blank=True, null=True)
    date1 = models.CharField(verbose_name="数据一", max_length=255, blank=True, null=True)
    choice_mode = (
        (1, '全部'),
        (2, '是'),
        (3, '否'),
    )
    is_xuxu = models.IntegerField(verbose_name="是否应用到讯讯", choices=choice_mode, default=1)
    is_sousou = models.IntegerField(verbose_name="是否应用到搜搜", choices=choice_mode, default=1)
    many_choice_mode = (
        (1, '链接'),
        (2, "网站"),
        (3, "二级版面"),
        (4, "三级版面"),
        (5, "危机APP别称"),
        (6, "搜搜别称"),
        (7, "网站类型"),
        (8, "地域"),
    )
    many_choice = models.IntegerField(verbose_name="链接", choices=many_choice_mode)



    class Meta:

        db_table = 'mx_medialibary'

