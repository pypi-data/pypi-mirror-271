from marshmallow import Schema, fields, validate

from ebb_events.enums import EventType


TOPIC_MAX_LENGTH = 50
TOPIC_REGEX = r"^[a-z0-9-]+$"
SOURCE_REGEX = r"^([a-z0-9-]+\/){4}[a-z0-9-]+$"
SOURCE_MAX_LENGTH = 256


class EventEnvelopeSchema(Schema):
    """Schema for EventEnvelope class to validate fields follow requirements"""

    organization = fields.Str(
        validate=[
            validate.Length(max=TOPIC_MAX_LENGTH),
            validate.Regexp(regex=TOPIC_REGEX),
        ]
    )
    system_id = fields.Str(
        validate=[
            validate.Length(max=TOPIC_MAX_LENGTH),
            validate.Regexp(regex=TOPIC_REGEX),
        ]
    )
    event_type = fields.Str(
        validate=[
            validate.Length(max=TOPIC_MAX_LENGTH),
            validate.OneOf([e.value for e in EventType]),
        ]
    )
    subsystem_id = fields.Str(
        validate=[
            validate.Length(max=TOPIC_MAX_LENGTH),
            validate.Regexp(regex=TOPIC_REGEX),
        ]
    )
    device_id = fields.Str(
        validate=[
            validate.Length(max=TOPIC_MAX_LENGTH),
            validate.Regexp(regex=TOPIC_REGEX),
        ]
    )


class RawToStringField(fields.Raw):
    """
    Class for our EventPayloadSchema id field to accept any id but returns
    that id as a string value e.g. (str(id))
    """

    def _serialize(self, value, attr, obj, **kwargs):
        return str(value)


class EventPayloadSchema(Schema):
    """Schema for event payload json to validate fields follow requirements"""

    # id field could be uuid but doesn't have to be (could be string(int))
    id = RawToStringField(required=True)
    time = fields.DateTime(required=True, format="iso")
    source = fields.Str(
        required=True,
        validate=[
            validate.Length(max=SOURCE_MAX_LENGTH),
            validate.Regexp(regex=SOURCE_REGEX),
        ],
    )
    type = fields.Str(
        required=True,
        validate=[
            validate.OneOf([e.value for e in EventType]),
        ],
    )
    data = fields.Dict(required=True)
