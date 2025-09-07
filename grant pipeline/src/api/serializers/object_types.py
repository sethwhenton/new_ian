#!/usr/bin/python3
"""Object_type schema module"""
from marshmallow import Schema, fields


class ObjectTypeSchema(Schema):
    """ObjectType Schema
            Responsible for data serialization, deserialization and validation
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
