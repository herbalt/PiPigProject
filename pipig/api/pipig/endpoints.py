from flask import request, abort
from flask_restplus import Resource
from flask_restplus import abort
from pipig.api import api as api_plus

from pipig.api.pipig.serializers import serial_pipig, serial_pipig_config, serial_pipig_snapshot
from pipig.api.pipig.business import configure_pipig
from pipig.pi_gpio.models import RaspberryPi

pipig_namespace = api_plus.namespace('pipig', description='PiPig is the core API that controllers the application')


@pipig_namespace.route('/config')
class PiPigConfig(Resource):

    @pipig_namespace.marshal_with(serial_pipig)
    def get(self):
        """
        Get the current setup in PiPig Operation.
        """
        pass

    @pipig_namespace.expect(serial_pipig_config)
    @pipig_namespace.marshal_with(serial_pipig)
    def post(self):
        """
        Configures the current Operation setup for PiPig.
        Requires {Recipe, Raspberry PI, Session Name}
        :return:
        """

        data = request.json
        pipig = configure_pipig(data)
        pipig_json = pipig.get_json()
        if pipig_json is None:
            abort(400, "The Recipe did not get created due to invalid values")
        return pipig_json, 201


@pipig_namespace.route('/snapshot')
class PiPigSnapshot(Resource):

    @pipig_namespace.marshal_with(serial_pipig_snapshot)
    def get(self):
        """
        Returns a full snapshot of the latest state of the PiPig Operation
        :return:
        """
        pass

@pipig_namespace.route('/snapshot/<float:time_elapsed>')
class PiPigSnapshotPoint(Resource):

    @pipig_namespace.marshal_with(serial_pipig_snapshot)
    def get(self, time_elapsed):
        """

        :return:
        """
        pass