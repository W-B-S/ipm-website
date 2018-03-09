#!usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time
from datetime import datetime, timedelta

DAY_SECOND = 24 * 60 * 60


def time_to_string_for_before(date_time, use_ch_date_format=False):
    now_time = datetime.now()
    timedelta = now_time - date_time
    t_seconds = timedelta.days * 24 * 3600 + timedelta.seconds

    if t_seconds < 60:
        if t_seconds < 0:
            t_result = date_time.strftime('%Y-%m-%d %H:%M:%S')
        elif t_seconds <= 10:
            t_result = u"刚刚"
        else:
            t_result = str(t_seconds / 10 * 10) + u"秒前"
    else:
        if t_seconds / 60 <= 60:
            t_result = str(t_seconds / 60) + u"分钟前"
        elif t_seconds / 60 / 60 < 24:
            t_result = str(t_seconds / 60 / 60) + u"小时前"
        else:
            if use_ch_date_format:
                t_result = u'{0}年{1}月{2}日'.format(
                    date_time.year, date_time.month, date_time.day
                )
            else:
                t_result = date_time.strftime('%Y-%m-%d')
    return t_result


def str_time_string_for_before(str_time):
    date_time = str_time_to_datetime(str_time)
    return time_to_string_for_before(date_time)


def timestamp_to_string_for_before(timestamp):
    date_time = get_date_time_from_timestamp(timestamp)
    return time_to_string_for_before(date_time)


def is_leap_year(year_num):
    if year_num % 100 == 0:
        if year_num % 400 == 0:
            return True
        else:
            return False
    else:
        if year_num % 4 == 0:
            return True
        else:
            return False


def str_time_to_datetime(str_time, format_str='%Y-%m-%d %H:%M:%S'):
    if isinstance(str_time, datetime):
        return str_time
    if format_str.startswith('%Y-%m-%d'):
        year, month, day = str_time.split(' ')[0].split('-')
        year = int(year)
        month = int(month)
        day = int(day)
        if day == 31 and month in (4, 6, 9, 11):
            day = 30
        if day > 28 and month == 2:
            day = 29 if is_leap_year(year) else 28
        if day < 10:
            day = '0{}'.format(day)
        if month < 10:
            month = '0{}'.format(month)
        new_day_str_time = '{}-{}-{}'.format(year, month, day)
        str_time = re.sub('\d{4}\-\d+\-\d{2}', new_day_str_time, str_time)
    dt = datetime.strptime(str_time, format_str)
    return dt


def datetime_to_str_time(date, format_str='%Y-%m-%d %H:%M:%S'):
    return date.strftime(format_str)


def get_now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_now():
    return datetime.now()


def get_timestamp(date_time=None):
    if not date_time:
        date_time = datetime.now()
    return int(time.mktime(date_time.timetuple()))


def get_date_time_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp)


def get_hour():
    return datetime.now().strftime('%H')


def to_tomorrow_second():
    return 86400 - (int(time.time()) - time.timezone) % 86400


def get_today_str(only_date=False):
    if only_date:
        return get_now_str()[:10]
    return get_now_str()[:10] + ' 00:00:00'


def get_date_time_delta(date_time, days=0, hours=0, minutes=0,
                        seconds=0):
    return date_time + timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds
    )


def get_today_zero_datetime():
    today_zero_str = get_today_str()
    today_zero_datetime = str_time_to_datetime(today_zero_str)
    return today_zero_datetime


# def get_one_day_time_zone():
#     """
#     获取昨天凌晨到今天凌晨的时间戳列表：['2017-07-13 00:00:00', '2017-07-14 00:00:00']
#     :return: tuple[str]
#     """
#     today = datetime.now()
#     yesterday = today - timedelta(days=1)
#     today_format = today.strftime('%Y-%m-%d %H:%M:%S')[:11]+'00:00:00'
#     yesterday_format = yesterday.strftime('%Y-%m-%d %H:%M:%S')[:11]+'00:00:00'
#     zone = (yesterday_format, today_format)
#     return zone


def get_one_day_time_zone():
    """
    获取昨天凌晨到今天凌晨的时间戳列表：['2017-07-13 00:00:00', '2017-07-14 00:00:00']
    :return: tuple[str]
    """
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d 00:00:00'), datetime.now().strftime('%Y-%m-%d 00:00:00')


# def get_one_hour_time_zone():
#     """
#     获取前一小时的时间戳列表：['2017-07-17 10:00:00', '2017-07-17 09:00:00']
#     :return: tuple[str]
#     """
#     now = datetime.now()
#     one_hour_ago = now - timedelta(minutes=60)
#     now_format = now.strftime('%Y-%m-%d %H:%M:%S')[:13]+':00:00'
#     one_hour_ago_format = one_hour_ago.strftime('%Y-%m-%d %H:%M:%S')[:13]+':00:00'
#     zone = (one_hour_ago_format, now_format)
#     return zone


def get_one_hour_time_zone():
    """
    获取前一小时的时间戳列表：['2017-07-17 10:00:00', '2017-07-17 09:00:00']
    :return: tuple[str]
    """
    one_hour_ago = datetime.now() - timedelta(hours=1)
    return one_hour_ago.strftime('%Y-%m-%d %H:00:00'), datetime.now().strftime('%Y-%m-%d %H:00:00')


def get_yesterday_str(only_date=False):
    yesterday = get_now() + timedelta(days=-1)
    result = datetime_to_str_time(yesterday, '%Y-%m-%d 00:00:00')
    if only_date:
        return result[:10]
    else:
        return result


def get_yesterday_datetime():
    return str_time_to_datetime(get_yesterday_str())


def get_last_hour_str():
    target_date_time = get_date_time_delta(get_now(), hours=-1)
    return datetime_to_str_time(target_date_time)


if __name__ == '__main__':
    print get_one_day_time_zone()
    print get_date_time_delta(get_now(), seconds=-31 * 6 * 86400)
