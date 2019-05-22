# -*- coding: utf-8 -*-


def ensure_str(s, encoding="utf-8"):
    if isinstance(s, unicode):
        return s.encode(encoding, "ignore")
    return str(s)


def ensure_unicode(s, encoding="utf-8"):
    if isinstance(s, unicode):
        return s
    return str(s).decode(encoding)
