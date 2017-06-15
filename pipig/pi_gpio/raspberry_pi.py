from pi_gpio.config import GPIO

from pipig.pi_gpio.models import RaspberryPi, GpioPin

PI_1_MODEL_B_REVISION_1 = "Pi 1 Model B Revision 1"
PI_1_MODEL_AB_REVISION_2 = "Pi 1 Model A/B Revision 2"
PI_1_MODEL_B_PLUS = "Pi 1 Model B+"
PI_1_MODEL_A_PLUS = "Pi 1 Model A+"
PI_2_MODEL_B = "Pi 2 Model B"
PI_MODEL_3 = "Pi 3 Model"
PI_MODEL_ZERO = "Pi Zero"


class BaseRaspberryPi:
    model_object = None
    dict_map = None
    configured = False

    def __init__(self, pi_model):
        self.pi_model = pi_model

    def obj_rasp_pi(self):
        if self.model_object is None:
            self.model_object = RaspberryPi.query.filter_by(name=self.pi_model).first()
        return self.model_object

    def __get_pin_count(self):
        return self.obj_rasp_pi().get_pin_count()

    def map_pins_to_dict(self):
        """
        Build a map of {PinPosition, Gpio Object, Gpio State Machine}
        Loop through range of integers for pin count
            Get the GPIO pin object from the Database
            Attach a new state machine for the pin
            Add to Dict
        :return: Dictionary Object {PinPosition, Gpio Object, Gpio State Machine}
        """
        if self.dict_map is None:
            pin_dict = {}

            for i in range(0, self.__get_pin_count()):
                if not pin_dict.has_key(i):
                    pin = GpioPin.query.filter_by(pin_position=i).first()
                    pin_dict[i] = pin
            self.dict_map = pin_dict

        return self.dict_map

    def configure_application(self, input_pin_list=None, output_pin_list=None):
        """

        :param input_pin_list: List of Pin Positions that will require configuration for GPIO Input
        :param output_pin_list: List of Pin Positions that will require configuration for GPIO Output
        :return:
        """
        for input_pin in input_pin_list:
            if input_pin is not None:
                GPIO.setup(input_pin, GPIO.IN)

        for output_pin in output_pin_list:
            if output_pin is not None:
                GPIO.setup(output_pin, GPIO.OUT)

        self.configured = True

