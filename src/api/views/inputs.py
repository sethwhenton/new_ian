#!/usr/bin/python3
"""
Input Views module
"""
from flask_restful import Resource
from ...storage import engine, Input
from ..serializers.inputs import InputSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, jsonify, make_response


input_schema = InputSchema(unknown=EXCLUDE)
inputs_schema = InputSchema(many=True)


class InputList(Resource):
    """Implements requests to for model predictions
        and stores them in database
    """
    def get(self):
        """returns all inputs with relevant details"""
        inputs = engine.all(Input)
        if not inputs:
            response = {
                "status": "error",
                "message": "could not fetch data from the storage",
                "data": inputs
            }
            return make_response(jsonify(response), 400)
        return inputs_schema.dump(inputs), 200

    def post(self):
        """retrieve information from the request object.
            ** pass the information to the model for prediction
            ** Post the prediction and information to the database
        Return: input information
        """
        data = request.get_json()
        try:
            data = input_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 403)

        new_input = Input(**data)
        # TO-DO 
        # Must consider Batch processing
        # model prediction and adding data to the output table
        # remember to improve output schema in order to output nested information
        new_input.save()

        return input_schema.dump(new_input), 201

class InputSingle(Resource):
    """Retrieves a single Input, deletes a Input
        and makes changes to an exisiting Input
    """
    def get(self, input_id):
        """retrive a single Input from the storage
        Arg:
            input_id: ID of the Input to retrieve
        """
        input = engine.get(Input, id=input_id)
        if input:
            return (input_schema.dump(input), 200)

    def delete(self, input_id):
        """Delete Input
        Arg:
            input_id: ID of the Input to be deleted
        """
        input = engine.get(Input, id=input_id)
        engine.delete(input)
        response = {'message': 'resource successfully deleted'}
        return make_response(jsonify(response), 200)

    def put(self, input_id):
        """Make changes to an existing Input
        Arg:
            input_id: ID of the Input to be changed
        """
        data = request.get_json()
        try:
            data = input_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 403)
        input = engine.update(Input, input_id, **data)
        return input_schema.dump(input), 200
