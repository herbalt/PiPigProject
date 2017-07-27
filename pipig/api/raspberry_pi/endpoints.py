from flask import request, abort
from flask_restplus import Resource
from flask_restplus import abort
from pipig.api import api as api_plus

from pipig.api.raspberry_pi.serializers import serial_pi
from pipig.pi_gpio.models import RaspberryPi

pi_namespace = api_plus.namespace('pis', description='The Raspberry PI device allows for interaction with the real world')


@pi_namespace.route('/')
class RaspberryPiDevices(Resource):

    @pi_namespace.marshal_list_with(serial_pi)
    def get(self):
        """
        Get all the available Raspberry PI devices to allow selection of the device in use.
        Will provide details on each GPIO pin that is available to the device in JSON Format.
        :return:
        """
        raspberry_pis = RaspberryPi.query.all()
        result_list = []
        for pi in raspberry_pis:
            result = pi.get_json()
            if result is not None:
                result_list.append(result)
        return result_list, 200


@pi_namespace.route('/<int:pi_id>')
class RaspberryPiItem(Resource):

    @pi_namespace.marshal_with(serial_pi)
    def get(self, pi_id):
        """
        Get all the available Raspberry PI devices to allow selection of the device in use.
        Will provide details on each GPIO pin that is available to the device in JSON Format.

        pi_id is the Raspberry PI model name to query
        """
        pi = RaspberryPi.get(pi_id)
        if pi is None:
            abort(500)
        return pi.get_json()



