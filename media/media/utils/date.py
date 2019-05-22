# -*- coding: utf-8 -*-
from datetime import date, timedelta, datetime


def date_range(basedate, days, reversed=False):
    range_list = range(0, days) if reversed else range(days - 1, -1, -1)
    return [basedate - timedelta(days=x) for x in range_list]


def date_list(start_date, end_date, reversed=False):
    days = (end_date - start_date).days + 1
    if days < 1:
        return []
    range_list = range(0, days) if reversed else range(days - 1, -1, -1)
    return [end_date - timedelta(days=x) for x in range_list]


def strpdate(str_date, format='%Y-%m-%d'):
    return datetime.strptime(str_date, format).date()


def getEveryDay(begin_date, end_date):
    date_list = []
    begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += timedelta(days=1)
    return date_list
