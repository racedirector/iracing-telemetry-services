import datetime


def DateEncoder(obj):
    """JSON encoder for datetime objects."""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()