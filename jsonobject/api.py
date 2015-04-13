from __future__ import absolute_import
from .base import JsonObjectBase, _LimitedDictInterfaceMixin

import decimal
import datetime

from . import properties as _properties
import re
import six


re_date = re.compile(r'^(\d{4})\D?(0[1-9]|1[0-2])\D?([12]\d|0[1-9]|3[01])$')
re_time = re.compile(
    r'^([01]\d|2[0-3])\D?([0-5]\d)\D?([0-5]\d)?\D?(\d{3,6})?$')
re_datetime = re.compile(
    r'^(\d{4})\D?(0[1-9]|1[0-2])\D?([12]\d|0[1-9]|3[01])'
    r'(\D?([01]\d|2[0-3])\D?([0-5]\d)\D?([0-5]\d)?\D?(\d{3,6})?'
    r'([zZ]|([\+-])([01]\d|2[0-3])\D?([0-5]\d)?)?)?$'
)
re_decimal = re.compile('^(\d+)\.(\d+)$')


class JsonObject(JsonObjectBase, _LimitedDictInterfaceMixin):
    def __getstate__(self):
        return self.to_json()

    def __setstate__(self, dct):
        self.__init__(dct)

    class Meta(object):
        properties = {
            decimal.Decimal: _properties.DecimalProperty,
            datetime.datetime: _properties.DateTimeProperty,
            datetime.date: _properties.DateProperty,
            datetime.time: _properties.TimeProperty,
            str: _properties.StringProperty,
            six.text_type: _properties.StringProperty,
            bool: _properties.BooleanProperty,
            float: _properties.FloatProperty,
            list: _properties.ListProperty,
            dict: _properties.DictProperty,
            set: _properties.SetProperty,
        }

        for integer_type in six.integer_types:
            properties[integer_type] = _properties.IntegerProperty

        string_conversions = (
            (re_date, datetime.date),
            (re_time, datetime.time),
            (re_datetime, datetime.datetime),
            (re_decimal, decimal.Decimal),
        )
