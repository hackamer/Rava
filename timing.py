from imports import *

def get_shamsi_date_str():
    """
    Return current date in Shamsi (Jalali) format as YYYY/MM/DD.
    """
    now = datetime.now()
    shamsi_now = jdatetime.datetime.fromgregorian(datetime=now)
    return f"{shamsi_now.year:04d}/{shamsi_now.month:02d}/{shamsi_now.day:02d}"


def get_shamsi_time_str():
    """
    Return current time as HH:MM:SS in Shamsi (Jalali) calendar.
    """
    now = datetime.now()
    shamsi_now = jdatetime.datetime.fromgregorian(datetime=now)
    return f"""{
        shamsi_now.hour:02d}:{
        shamsi_now.minute:02d}:{
            shamsi_now.second:02d}"""


if __name__ == "__main__":
    print(get_shamsi_date_str())
    print(get_shamsi_time_str())
    raise RavaAppError("Please Dont run this file run main.py file")
