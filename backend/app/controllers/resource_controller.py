from flask import jsonify, request
from . import api
from ..database import Resource
from ..utils import json_load, check_json, check_outside


@api.route('/resources')
def get_resources():
    resources = Resource.query.all()
    return jsonify([{
        'id': resource.id,
        'name': resource.name
    } for resource in resources])


@api.route('/resources/free', methods=['POST'])
def get_free_resources():
    json = json_load(request.json)
    check_json(json, ['start', 'end'])
    free_resources = []
    _resources = Resource.query.all()
    for res in _resources:
        valid = True
        for event in res.events:
            if not check_outside(event, json):
                valid = False
                break
        if valid:
            free_resources.append(res)
    return jsonify([{
        "id": res.id,
        "name": res.name,
        "kind": res.kind
    } for res in free_resources])


@api.route('/resources/<int:id>')
def get_resource(id):
    resource = Resource.query.get_or_404(id)
    events = [{'id': event.id, 'title': event.title} for event in resource.events]
    return jsonify({
        'id': resource.id,
        'name': resource.name,
        'events': events
    })
