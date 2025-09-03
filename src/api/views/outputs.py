#!/usr/bin/python3
"""
Output Views module
"""
from flask_restful import Resource
from ...storage import engine, Output
from ..serializers.outputs import OutputSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, jsonify, make_response


output_schema = OutputSchema(unknown=EXCLUDE)
outputs_schema = OutputSchema(many=True)


class OutputList(Resource):
    """Implements requests to for model predictions
        and stores them in database
    """
    def get(self):
        """returns all ouputs with relevant details"""
        outputs = engine.all(Output)
        if not outputs:
            response = {
                "status": "error",
                "message": "could not fetch data from the storage",
                "data": outputs
            }
            return make_response(jsonify(response), 400)
        return outputs_schema.dump(outputs), 200

    # This function may not be necessary since we are posting directly to the inputs table using the Input views
    def post(self):
        """retrieve information from the request object.
            ** Post output information to the database
        Return: the output information
        """
        data = request.get_json()
        try:
            data = output_schema.load(data)
            data = output_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 403)

        new_output = Output(**data)
        engine.new(new_output)
        engine.save()

        return output_schema.dump(new_output), 201

class OutputSingle(Resource):
    """Retrieves a single Output, deletes a Output
        and makes changes to an exisiting Output
    """
    def get(self, output_id):
        """retrive a single Output from the storage
        Arg:
            output_id: ID of the Output to retrieve
        """
        output = engine.get(Output, id=output_id)
        if output:
            return (output_schema.dump(output), 200)

    def delete(self, output_id):
        """Delete Output
        Arg:
            output_id: ID of the Output to be deleted
        """
        output = engine.get(Output, id=output_id)
        engine.delete(output)
        response = {'message': 'resource successfully deleted'}
        return make_response(jsonify(response), 200)

    def put(self, output_id):
        """Make changes to an existing Output
        Arg:
            output_id: ID of the Output to be changed
        """
        data = request.get_json()
        try:
            data = output_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 403)
        output = engine.update(Output, output_id, **data)
        return output_schema.dump(output), 200
