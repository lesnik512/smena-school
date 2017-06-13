import re
from datetime import timedelta


def get_mon_fri_of_current_week(today):
    monday_date = today + timedelta(days=0 - today.weekday())
    friday_date = today + timedelta(days=4 - today.weekday())
    return monday_date, friday_date


def sms_code_is_valid(sms_code):
    return True


def clean_phone(dirty_phone):
    r = re.match(r'\+7\((\d+)\).(\d+)-(\d+)', dirty_phone)
    return ''.join(r.groups())