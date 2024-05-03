import datetime


def get_timestamp_for_paths():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%dT%H_%M_%S")
