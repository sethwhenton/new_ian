#!/usr/bin/python3
"""Output schema module"""
from marshmallow import Schema, fields, validates, ValidationError


class OutputSchema(Schema):
    """Output Schema for data serialization
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    predicted_count = fields.Integer(required=True)
    corrected_count = fields.Integer(required=True)
    pred_confidence = fields.Float(required=True)
    object_type_id = fields.Str()
    input_id = fields.Str()
