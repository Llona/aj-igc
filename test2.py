from crawler import DateTimeControl
import re

time_string = '2020-01-06T12:36:02.000Z'
time_string = re.sub('.000Z', '', time_string)
datetime_control = DateTimeControl()
date_time = datetime_control.change_string_to_utc_datetime(time_string, 'Asia/Taipei')
print(date_time)
