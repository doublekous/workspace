# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paging_handle(items, page=1, length=10):
    """
        :param items: list
        :param page:  current page number
        :param length: number per page
        :return:  paginator.page(paginator.num_pages)
    """
    paginator = Paginator(items, length)  # Show 10 notifications per page
    try:
        page = int(page)
        current_page = paginator.page(page)
        last_page_num = paginator.page_range[-1]  # last page
        # get page number list eg. [1,-1,curent_page-4,...,curent_page,...curent_page+4,-1,last_page]
        step = 4
        begin = max(1, page - step)
        end = min(last_page_num, page + step)
        ran = range(begin, end + 1, 1)
        if ran[0] > 2:
            ran.insert(0, -1)
        if ran[0] != 1:
            ran.insert(0, 1)
        if ran[-1] < last_page_num - 1:
            ran.append(-1)
        if ran[-1] != last_page_num:
            ran.append(last_page_num)
        paginator.page_range_custom = ran

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        # current_page = paginator.page(paginator.num_pages)
        current_page = None
    return current_page


class Pagenate(object):
    def __init__(self, page_num, all_items, items_per_page=10, page_step=2):
        self.page_num = page_num
        self.all_items = all_items
        self.items_per_page = items_per_page
        self.page_step = page_step

    def page_range_custom(self, max_page_num):
        # get page number list eg. [1,-1,curent_page-4,...,curent_page,...curent_page+4,-1,last_page]
        begin = max(1, self.page_num - self.page_step)
        end = min(max_page_num, self.page_num + self.page_step)
        page_range = range(begin, end + 1, 1)
        if page_range[0] > 2:
            page_range.insert(0, -1)
        if page_range[0] != 1:
            page_range.insert(0, 1)
        if page_range[-1] < max_page_num - 1:
            page_range.append(-1)
        if page_range[-1] != max_page_num:
            page_range.append(max_page_num)
        return page_range

    def json_result(self):
        items = self.result()
        return {
            'num_pages': items.paginator.num_pages,
            'has_previous': items.has_previous(),
            'previous_page_number': items.previous_page_number() if items.has_previous() else 1,
            'has_next': items.has_next(),
            'next_page_number': items.next_page_number() if items.has_next() else 1,
            'page_range_custom': items.paginator.page_range_custom,
            'number': items.number,
        }

    def result(self):
        paginator = Paginator(self.all_items, self.items_per_page)  # Show 10 notifications per page

        try:
            paginator.page_range_custom = self.page_range_custom(paginator.page_range[-1])

            items = paginator.page(self.page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)
        return items
