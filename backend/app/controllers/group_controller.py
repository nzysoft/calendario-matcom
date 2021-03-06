from flask import jsonify, request
from . import api
from ..database import Group
from ..utils import json_load, check_json, check_inside


@api.route('/groups')
def get_groups():
    groups = Group.query.all()
    return jsonify([{
        'id': group.id,
        'name': group.name
    } for group in groups])


@api.route('/groups/<int:id>')
def get_group(id):
    group = Group.query.get_or_404(id)
    events = [{'id': event.id, 'title': event.title} for event in group.events]
    users = [{'id': user.id, 'username': user.username} for user in group.users]
    return jsonify({
        'id': group.id,
        'name': group.name,
        'events': events,
        'users': users
    })


@api.route('/groups/free')
def get_free_classes():
    json = json_load(request.json)
    check_json(json, ['groups', 'start', 'end'])
    times = []
    for group_id in json.groups:
        group = Group.query.filter_by(id=group_id).first()
        for event in group.events:
            if check_inside(event, json):
                times.append((max(event.start, json.start), "start"))
                times.append((min(event.end, json.end), "end"))
    times.append((json.start, "start"))
    times.append((json.end, "end"))
    times.sort(key=lambda j: j[0])

    free_time_intervals = []
    balance = 0
    start_of_interval = times[0][0]
    end_of_interval = times[0][0]
    for i in range(0, len(times)):
        if balance == 1:
            end_of_interval = times[i][0]
            if start_of_interval != end_of_interval:
                free_time_intervals.append((start_of_interval, end_of_interval))
        if times[i][1] == "end":
            balance -= 1
        else:
            balance += 1
        if balance == 1:
            start_of_interval = times[i][0]

    return jsonify([
        {
        "start": interval[0],
        "end": interval[1]
        }
        for interval in free_time_intervals
        ])