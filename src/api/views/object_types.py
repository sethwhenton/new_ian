#!/usr/bin/python3
"""
ObjectType Views module
"""
from flask_restful import Resource
from ...storage import engine, ObjectType
from ..serializers.object_types import ObjectTypeSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, jsonify, make_response


obj_schema = ObjectTypeSchema(unknown=EXCLUDE)
objs_schema = ObjectTypeSchema(many=True)

class ObjectTypeList(Resource):
    """Implements requests to for model predictions
        and stores them in database
    """
    def get(self):
        """returns all object_types with relevant details"""
        objs = engine.all(ObjectType)
        if not objs:
            response = {
                "status": "error",
                "message": "could not fetch data from the storage",
                "data": objs
            }
            return make_response(jsonify(response), 400)
        return objs_schema.dump(objs), 200

    def post(self):
        """retrieve information from the request object.
        Return: Object Type information
        """
        data = request.get_json()
        try:
            data = obj_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 403)

        new_obj = ObjectType(**data)
        new_obj.save()

        return obj_schema.dump(new_obj), 201

class ObjectTypeSingle(Resource):
    """Retrieves a single Object Type, deletes a Object Type
        and makes changes to an exisiting Object Type
    """
    def get(self, obj_id):
        """retrive a single Object Type from the storage
        Arg:
            obj_id: ID of the Object Type to retrieve
        """
        obj = engine.get(ObjectType, id=obj_id)
        if obj:
            return (obj_schema.dump(obj), 200)

    def delete(self, obj_id):
        """Delete Object Type
        Arg:
            obj_id: ID of the Object Type to be deleted
        """
        obj = engine.get(ObjectType, id=obj_id)
        engine.delete(obj)
        response = {'message': 'resource successfully deleted'}
        return make_response(jsonify(response), 200)

    def put(self, obj_id):
        """Make changes to an existing Object Type
        Arg:
            obj_id: ID of the Object Type to be changed
        """
        data = request.get_json()
        try:
            data = obj_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 403)
        obj = engine.update(ObjectType, obj_id, **data)
        return obj_schema.dump(obj), 200
