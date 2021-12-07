from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class UserSchema(Schema):
    username = fields.String(validate=Length(min=5))
    firstName = fields.String(validate=Length(min=3))
    lastName = fields.String(validate=Length(min=3))
    password = fields.String(validate=Length(min=8))
    email = fields.Email()
    phone = fields.Number()

class TicketSchema(Schema):
    eventId = fields.Integer()

class EventSchema(Schema):
    name = fields.String(validate=Length(min=5))
    date = fields.Date()

