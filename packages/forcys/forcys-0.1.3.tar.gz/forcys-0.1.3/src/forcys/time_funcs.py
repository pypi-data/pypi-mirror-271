from datetime import datetime


def timestring(time):
    return datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')