from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime
from models import Event, User, Ticket
from srenshin import session
from validation_schemas import EventSchema

event = Blueprint('event', __name__)
bcrypt = Bcrypt()


@event.route('/api/v1/event', methods=['POST'])
def create_event():
    data = request.get_json(force=True)
    
    try:
        EventSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 405
  
    newEvent = Event(name=data["name"], date=data["date"])
    session.add(newEvent)
    session.commit()
    session.close()
    return Response(response='New event was successfully created!')


@event.route('/api/v1/event/getAvailableEvents', methods=['GET'])
def get_available_events():
    events = session.query(Event)
    event_data = []
    for event in events:
        event_data.append(
            {
            'id': event.id, 
            'name': event.name, 
            'date': event.date
            }
        )
    return jsonify(event_data)


@event.route('/api/v1/event/availableTickets/<eventId>', methods=['GET'])
def get_event_tickets(eventId):
    tickets = session.query(Ticket).filter_by(eventId=eventId)
    if not event:
        return Response(status=404, response='A event with provided id was not found.')
    if not tickets:
        return Response(status=404, response='A event with provided id has no tickets.')
    tickets = [ticket.id for ticket in tickets]

    return jsonify({"tickets": tickets})
