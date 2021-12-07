from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime
from models import Ticket, User, Event
from srenshin import session
from validation_schemas import TicketSchema

ticket = Blueprint('ticket', __name__)
bcrypt = Bcrypt()


@ticket.route('/api/v1/ticket', methods=['POST'])
def create_ticket():
    data = request.get_json(force=True)
    
    try:
        TicketSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 405
    event = session.query(Event).filter_by(id=data["eventId"]).first()
    if not event:
        return Response(status=404, response='A event with provided id was not found.')
    newTicket = Ticket(eventId = data["eventId"])
    session.add(newTicket)
    session.commit()
    session.close()

    return Response(response='New ticket was successfully created!')


@ticket.route('/api/v1/ticket/<ticketId>', methods=['GET'])
def get_ticket(ticketId):
    ticket = session.query(Ticket).filter_by(id=ticketId).first()
    if not ticket:
        return Response(status=404, response='A ticket with provided id was not found.')
    
    ticket_data = {
            'id': ticket.id,
            'userId': ticket.userId,
            'eventId': ticket.eventId, 
            'isBooked': ticket.isBooked, 
            'isBought': ticket.isBought
            }

    return jsonify(ticket_data)

@ticket.route('/api/v1/ticket/<ticketId>/buy/<userId>', methods=['PUT'])
def buy_ticket(ticketId, userId):
    ticket = session.query(Ticket).filter_by(id=ticketId).first()
    if not ticket:
        return Response(status=404, response='A ticket with provided id was not found.')
    
    user = session.query(User).filter_by(id=userId).first()
    if not user:
        return Response(status=404, response='A user with provided id was not found.')
    
    if ticket.isBooked and ticket.userId != user.id:
        return Response(status=403, response='Ticket booked by not you.')

    if ticket.isBought:
        return Response(status=401, response='Ticket already bought.')

    ticket.isBought = True
    ticket.userId = user.id

    session.commit()
    session.close()

    return Response(response='Successfully bought')

@ticket.route('/api/v1/ticket/<ticketId>/book/<userId>', methods=['PUT'])
def book_ticket(ticketId, userId):
    ticket = session.query(Ticket).filter_by(id=ticketId).first()
    if not ticket:
        return Response(status=404, response='A ticket with provided id was not found.')
    
    user = session.query(User).filter_by(id=userId).first()
    if not user:
        return Response(status=404, response='A user with provided id was not found.')
    
    if ticket.isBooked:
        return Response(status=401, response='Ticket already booked.')

    if ticket.isBought:
        return Response(status=401, response='Ticket already bought.')

    ticket.isBooked = True
    ticket.userId = user.id

    session.commit()
    session.close()

    return Response(response='Successfully booked')

@ticket.route('/api/v1/ticket/<ticketId>/book', methods=['DELETE'])
def delete_book_ticket(ticketId):
    ticket = session.query(Ticket).filter_by(id=ticketId).first()
    if not ticket:
        return Response(status=404, response='A ticket with provided id was not found.')
    
    if not ticket.isBooked:
        return Response(status=401, response='Ticket not booked.')

    if ticket.isBought:
        return Response(status=401, response='Ticket bought.')

    ticket.isBooked = False
    ticket.userId = None

    session.commit()
    session.close()

    return Response(response='Successfully deleted')

@ticket.route('/api/v1/ticket/<ticketId>', methods=['PUT'])
def updateNote(ticketId):
    data = request.get_json(force=True)

    try:
        EditSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 405

    ticketData = session.query(Note).filter_by(id=ticketId).first()
    if not ticketData:
        return Response(status=404, response='The ticket with provided ID was not found.')
    exist = session.query(User).filter_by(id=data['editor']).first()
    if not exist:
        return Response(status=404, response='Editor does not exist.')
    newEdit = Edit(ticket=ticketId, editor=data['editor'], old_text=ticketData.text, new_text=data['new_text'],when_created = datetime.now())
    if 'new_text' in data.keys():
        ticketData.text = data['new_text']
    session.add(newEdit)
    session.commit()
    session.close()

    return Response(response='The ticket was updated.')

@ticket.route('/api/v1/ticket/<ticketId>', methods=['DELETE'])
def deleteNote(ticketId):
    ticketData = session.query(Note).filter_by(id=ticketId).first()
    if not ticketData:
        return Response(status=404, response='The ticket with provided ID was not found.')
    session.delete(ticketData)
    session.commit()
    session.close()
    return Response(response='The ticket was deleted.')