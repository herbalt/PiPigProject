from flask import request, abort
from flask_restplus import Resource
from flask_restplus import abort
from pipig.api import api as api_plus

from .serializers import serial_pipig, serial_pipig_config, serial_pipig_snapshot, serial_pipig_status
from .business import configure_pipig
from pi_gpio.models import RaspberryPi
from pi_pig.models import PiPigModel

pipig_namespace = api_plus.namespace('pipig', description='PiPig is the core API that controllers the application')


@pipig_namespace.route('/configurations')
class PiPigConfig(Resource):

    @pipig_namespace.marshal_list_with(serial_pipig)
    def get(self):
        """
        Get the all PiPig Configurations.
        \nThis will return a list of all the PiPig instances saved to the Database.
        \nThis should also allow visibility of if a Instance is currently in operation, based on its status

        """
        pipig_models = PiPigModel.query.all()
        result_list = []
        for pi_pig in pipig_models:
            result = pi_pig.get_json()
            if result is not None:
                result_list.append(result)
        return result_list, 200

    @pipig_namespace.expect(serial_pipig_config)
    @pipig_namespace.marshal_with(serial_pipig)
    def post(self):
        """
        Configuration for a new PiPig Instance.
        \nRequires existing database instances of {Recipe, Raspberry PI}
        \nConfigures the current Operation ready to start the PiPig Instance
        :return:
        """

        data = request.json
        pipig = configure_pipig(data)
        pipig_json = pipig.get_json()
        if pipig_json is None:
            abort(400, "The Recipe did not get created due to invalid values")
        return pipig_json, 201

    @pipig_namespace.route('/status/<int:pipig_id>')
    class PiPigStatusUpdate(Resource):

        @pipig_namespace.marshal_with(serial_pipig_status)
        def get(self, pipig_id):
            """
            Get current status of the PiPig instance
            :return:
            """
            pipig_model = PiPigModel.get(pipig_id)
            return pipig_model.get_status()


        def post(self, pipig_id):
            """
            Works out the type of Status Transition required on Server.
            STATUS TYPES based on PiPigStatus
            Performs Status Transition on Server.
            Respond with the new Status of the PiPig instance
            """
            pass

    # TODO Add a call to Post and Get Notes from a Session


    @pipig_namespace.route('/snapshot/<int:pipig_id>')
    class PiPigSnapshot(Resource):

        # @pipig_namespace.marshal_with(serial_pipig_snapshot)
        def get(self, pipig_id):
            """
            Returns a full snapshot of the all readings of the PiPig operation
            :return:
            """
            pass

# TODO Add a call to Post and Get Notes from a Session


