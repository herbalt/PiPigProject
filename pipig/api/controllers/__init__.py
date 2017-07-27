from flask import request, abort
from flask_restplus import Resource
from flask_restplus import abort
from pipig.api import api as api_plus

from pipig.api.controller.serializers import serial_controller, serial_controller_config, serial_snapshot
from pipig.pi_gpio.models import RaspberryPi

controller_namespace = api_plus.namespace('controllers', description='The application is operated by the Controller')


@controller_namespace.route('/config')
class PiPigConfig(Resource):

    @controller_namespace.marshal_with(serial_controller)
    def get(self):
        """
        Get the current setup in PiPig Operation.
        """
        pass

    @controller_namespace.expect(serial_controller_config)
    @controller_namespace.marshal_with(serial_controller)
    def post(self):
        """
        Configures the current Operation setup for PiPig.
        Requires {Recipe, Raspberry PI, Session Name}
        :return:
        """
        pass

@controller_namespace.route('/snapshot')
class PiPigSnapshot(Resource):

    @controller_namespace.marshal_with(serial_snapshot)
    def get(self):
        """
        Returns a full snapshot of the latest state of the PiPig Operation
        :return:
        """
        pass

@controller_namespace.route('/snapshot/<float:time_elapsed>')
class PiPigSnapshotPoint(Resource):

    @controller_namespace.marshal_with(serial_snapshot)
    def get(self, time_elapsed):
        """

        :return:
        """
        pass