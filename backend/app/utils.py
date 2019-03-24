from datetime import datetime, timedelta
from json import loads
from .exceptions import ValidationError


class AttributeDict(dict):

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


def check_json(json, required):
    for item in required:
        if item not in json:
            raise ValidationError(f'{item} es necesario.')


def json_load(json):
    json = loads(json) if isinstance(json, str) else json
    return AttributeDict(json)


def get_date(str_date):
    year = int(str_date.split('-')[0])
    month = int(str_date.split('-')[1])
    day = int(str_date.split('-')[2].split('T')[0])
    hour = int(str_date.split('T')[1].split(':')[0])
    minute = int(str_date.split('T')[1].split(':')[1])
    second = int(str_date.split('T')[1].split(':')[2].split('.')[0])
    return datetime(year, month, day, hour, minute, second) - timedelta(hours=4)


def merge(left, right):
    result = []
    ids = [item.id for item in right]
    for item in left:
        if item.id in ids:
            result.append(item)
    return result


def check_date(event, json):
    left = right = True
    if 'start' in json:
        left = get_date(json.start) <= event.start
    if 'end' in json:
        right = event.end <= get_date(json.end)
    return left and right


def query(items, events, attr):
    result = []
    if items:
        for event in events:
            for item in attr(event):
                if item.id in items:
                    result.append(event)
                    break
    else:
        result = events
    return result
