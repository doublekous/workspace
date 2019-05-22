# -*- coding: utf-8 -*-
import csv
import traceback


class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.

    """

    def __init__(self, f, dialect="excel", encoding="utf-8", **kwds):
        self.writer = csv.writer(f, dialect=dialect, **kwds)
        self.encoding = encoding

    def writerow(self, row):
        row = [(str(item) if not isinstance(item, basestring) else item) for item in row]
        row = [s.encode("gbk", "ignore") for s in row]
        self.writer.writerow(row)


class CSVDumper(object):
    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath
        self.f = None
        self.writer = None

    def process_item(self, item):

        try:
            if self.f is None:
                with open(self.csv_filepath, "ab+") as self.f:
                    self.writer = UnicodeWriter(self.f)
                    self.writer.writerow([i.split('__')[-1] for i in sorted(item.keys())])
                    self.writer.writerow([v for _, v in sorted(item.items())])
            else:
                with open(self.csv_filepath, "ab+") as self.f:
                    self.writer = UnicodeWriter(self.f)
                    self.writer.writerow([v for _, v in sorted(item.items())])
        except:
            print traceback.format_exc()
