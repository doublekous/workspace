# -*- coding: utf-8 -*-
import csv
import json
import os
import sys
import dateformatting
from StringIO import StringIO
import datetime
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_protect

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
from io import BytesIO
from urllib import quote

import time

import xlrd
import xlwt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

from media.settings import BASE_DIR
from medialibary.models import MediaLibrary


def get_style(name,color=0, bold=False, italic=False):
    """指定参数单元格式"""
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.colour_index = color
    font.bold = bold
    font.italic = italic
    style.font = font
    return style


def file_down(request):
    """下载模板"""
    path = os.path.join(BASE_DIR, 'static', 'download', 'model2.csv')
    file = open(path, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="model2.csv"'
    return response


@csrf_protect
def download_mode(request):
    """导入csv到数据库"""
    if request.method == 'GET':
        return render(request, 'medialibary/download_mode.html')
    if request.method == 'POST':
        file_obj = request.FILES.get('file_upload_trumpl')
        ori_name = file_obj.name
        if file_obj:
            time_stamp = int(time.time())
            file_name = os.path.join(
                BASE_DIR, 'static', 'upload', ("download_mode") + str(time_stamp)
            )
            # 写入到后台
            with open(file_name, 'wb') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            # 保存信心
            task_list = MediaLibrary.objects.all().order_by('-id')
            resu_data = []
            for tas in task_list:
                resu_data.append({
                    'id': tas.id,
                    'url': tas.url,
                    'secondpage': tas.secondpage,
                    'thirdpage': tas.thirdpage,
                    'xunxun_nickname': tas.xunxun_nickname,
                    'sousou_nickname': tas.sousou_nickname,
                    'website': tas.website,
                    'sitetype': tas.sitetype,
                    'regional': tas.regional,
                    'fetchlevel': tas.fetchlevel,
                    'yesterdaycapture': tas.yesterdaycapture,
                    'is_author': tas.is_author,
                    'addtime': tas.addtime.strftime('%Y-%m-%d %H:%M:%S') if tas.addtime else '',
                    'updatetime': tas.updatetime.strftime('%Y-%m-%d %H:%M:%S') if tas.updatetime else '',
                    'latestfetchtime': tas.latestfetchtime.strftime('%Y-%m-%d %H:%M:%S') if tas.latestfetchtime else '',
                    'fetchstatus': tas.fetchstatus,
                    'is_process': tas.is_process,
                    'note': tas.note,
                    'is_xuxu': tas.is_xuxu,
                    'is_sousou': tas.is_sousou,
                    'many_choice': tas.many_choice,
                })
            MediaLibrary.objects.create(id=tas.id, url=tas.url, secondpage=tas.secondpage, thirdpage=tas.thirdpage, xunxun_nickname=tas.xunxun_nickname,
                                        sousou_nickname=tas.sousou_nickname, website= tas.website, sitetype=tas.sitetype, regional=tas.regional,
                                        fetchlevel=tas.fetchlevel, yesterdaycapture=tas.yesterdaycapture, is_author=tas.is_author,
                                        addtime=tas.addtime, updatetime=tas.updatetime, latestfetchtime=tas.latestfetchtime,
                                        fetchstatus=tas.fetchstatus, is_process=tas.is_process, note=tas.note, is_xuxu=tas.is_xuxu, is_sousou=tas.is_sousou, many_choice=tas.many_choice)
            return HttpResponse(json.dumps({'resu_data': resu_data}))


def thread_get_sourcetype_media(task_dict, time_stamp, file_name):
    resu_file = os.path.join(
        BASE_DIR, 'static', 'download', ()
    )


def export_emp_excel(request):
    """导出Excel报表"""
    # 创建Excel工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    # 向工作簿中添加工作表
    sheet = workbook.add_sheet(u'models')
    # 设置表头
    titles = ('ID', '链接', '网站', '二级板面', '三级版面', '讯讯别称', '搜搜别称',  '网站类型', '地域', '抓取等级',
              '昨日抓取量', '是否有作者/互动/原创转载', '添加人', '添加时间', '修改时间', '最新抓取时间', '抓取状态',
              '作者/互动/原创转载是否处理', '是否应用讯讯', '是否应用搜搜',  '备注')
    props = ('id', 'url','website', 'secondpage', 'thirdpage', 'xunxun_nickname', 'sousou_nickname',
                 'sitetype', 'regional', 'fetchlevel', 'yesterdaycapture', 'is_author',
                 'addpaper', 'addtime', 'updatetime', 'latestfetchtime', 'fetchstatus', 'is_process',
                'is_xuxu', 'is_sousou','note')
    for col, title in enumerate(titles):
        sheet.write(0, col, title, get_style('Arial', color=2, bold=True))
        medialibrarys = MediaLibrary.objects.all().only(*props).order_by('yesterdaycapture')
    for row, medialibrary in enumerate(medialibrarys):
        for col, prop in enumerate(props):
            val = getattr(medialibrary, prop, '')
            if isinstance(val, MediaLibrary):
                val = val.name
            sheet.write(row + 1, col, val)
    # 提取Excel表格的数据
    buffer = StringIO()
    workbook.save(buffer)
    # 生成响应对象传输数据给浏览器
    resp = HttpResponse(buffer.getvalue())
    filename = 'models.csv'
    resp['Content-Type'] = 'application/csv'
    resp['content-disposition'] = 'attachment; filename="models.csv"'
    return resp













