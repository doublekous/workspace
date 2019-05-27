# -*- coding: utf-8 -*-
from django.db import models


class MediaLibrary(models.Model):
    url = models.CharField(verbose_name="链接", max_length=255)
    secondpage = models.CharField(verbose_name="二级面板", max_length=255, blank=True, null=True)
    thirdpage = models.CharField(verbose_name="三级面板", max_length=255, blank=True, null=True)
    xunxun_nickname = models.CharField(verbose_name="讯讯别称", max_length=255, blank=True, null=True)
    sousou_nickname = models.CharField(verbose_name="搜搜别称", max_length=255, blank=True, null=True)
    website = models.CharField(verbose_name="网站", max_length=255, blank=True, null=True)
    sitetype = models.CharField(verbose_name="网站类型", max_length=255, blank=True, null=True)
    regional = models.CharField(verbose_name="地域", max_length=255, blank=True, null=True)
    fetchlevel = models.IntegerField(verbose_name="抓取等级", choices=((1, '全部'), (2, '高'), (3, '中'), (4, '低')), blank=True, null=True)
    yesterdaycapture = models.IntegerField(verbose_name="昨日抓取量", blank=True, null=True)
    author_mode = (
        (1, '无'),
        (2, '有作者'),
        (3, '有互动'),
        (4, '有原创'),
        (4, '有转载'),

    )
    is_author = models.IntegerField(verbose_name="是否有作者/互动/原创",choices=author_mode,blank=True, null=True)
    addpaper = models.CharField(verbose_name="添加人", max_length=255, blank=True, null=True)
    addtime = models.DateTimeField(verbose_name="添加时间", auto_now_add=True,blank=True, null=True)
    updatetime = models.DateTimeField(verbose_name="修改时间", auto_now_add=True,blank=True, null=True)
    latestfetchtime = models.DateTimeField(verbose_name="最新抓取时间", auto_now_add=True, blank=True, null=True)
    fetchstatus = models.IntegerField(verbose_name="抓取状态", choices=((1, '全部'), (2, '失败'), (3, '完成')),blank=True, null=True)
    is_process = models.IntegerField(verbose_name="是否处理", choices=((1, '全部'),(2, '未处理'), (3, '已处理'), (4, '无')),blank=True, null=True)
    note = models.CharField(verbose_name="备注", max_length=255, blank=True, null=True)
    is_static = models.IntegerField(verbose_name="是否是静态",choices=((1, '是静态'), (2,'是动态')))
    choice_mode = (
        (1, '全部'),
        (2, '是'),
        (3, '否'),
    )
    is_xuxu = models.IntegerField(verbose_name="是否应用到讯讯", choices=choice_mode,blank=True, null=True, default=1)
    is_sousou = models.IntegerField(verbose_name="是否应用到搜搜", choices=choice_mode, blank=True, null=True, default=1)
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
    many_choice = models.IntegerField(verbose_name="链接", choices=many_choice_mode, blank=True, null=True)
    is_del = models.IntegerField(verbose_name="是否删除", choices=((1, '是'), (0, '否')), default=0, blank=True, null=True)
    count = models.IntegerField(verbose_name="修改量", blank=True, null=True)
    is_select = models.BooleanField(verbose_name="是否选中", default=False)

    class Meta:

        db_table = 'mx_medialibary'


