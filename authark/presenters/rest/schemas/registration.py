from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class RegistrationSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    enroll = fields.Boolean(default=False, missing=False)
    tenant = fields.Str(required=True, example="knowark")
    email = fields.Str(required=True, example="jarango@ops.servagro.com.co")
    username = fields.Str(required=True, example="jarango")
    password = fields.Str(required=True, example="secret")
    name = fields.Str(required=True, example="Jaime Arango")
    zone = fields.Str(example="default")
    attributes = fields.Mapping()
