from datetime import datetime, timedelta


def schedule(days=0, hours=0, minutes=0, seconds=0):
    total_seconds = days * 86400
    total_seconds += hours * 3600
    total_seconds += minutes * 60
    total_seconds += seconds
    return total_seconds


def seconds_to_date(seconds):
    return datetime.now() - timedelta(seconds=seconds)
