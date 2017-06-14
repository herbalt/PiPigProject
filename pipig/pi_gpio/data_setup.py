from pipig import app
from pipig.pi_gpio.models import GpioPin, RaspberryPi


def data_setup():
    gpio_data_setup()
    rasp_pi_data_setup()


def gpio_data_setup():
    with app.app_context():
        print str(helper_gpio_create(pin_position=1, pin_number=None, bcm_pin=None, pin_name="3v3 Power"))
        print str(helper_gpio_create(pin_position=2, pin_number=None, bcm_pin=None, pin_name="5V Power"))
        print str(helper_gpio_create(pin_position=3, pin_number=3, bcm_pin=2, pin_name="SDA"))
        print str(helper_gpio_create(pin_position=4, pin_number=None, bcm_pin=None, pin_name="5V Power"))
        print str(helper_gpio_create(pin_position=5, pin_number=5, bcm_pin=3, pin_name="SCL"))
        print str(helper_gpio_create(pin_position=6, pin_number=None, bcm_pin=None, pin_name="Ground"))
        print str(helper_gpio_create(pin_position=7, pin_number=7, bcm_pin=4, pin_name="GPCLK0"))
        print str(helper_gpio_create(pin_position=8, pin_number=8, bcm_pin=14, pin_name="TXD"))
        print str(helper_gpio_create(pin_position=9, pin_number=None, bcm_pin=None, pin_name="Ground"))
        print str(helper_gpio_create(pin_position=10, pin_number=10, bcm_pin=15, pin_name="RXD"))
        print str(helper_gpio_create(pin_position=11, pin_number=11, bcm_pin=17, pin_name=""))
        print str(helper_gpio_create(pin_position=12, pin_number=12, bcm_pin=18, pin_name="PWM0"))
        print str(helper_gpio_create(pin_position=13, pin_number=13, bcm_pin=27, pin_name=""))
        print str(helper_gpio_create(pin_position=14, pin_number=None, bcm_pin=None, pin_name="Ground"))
        print str(helper_gpio_create(pin_position=15, pin_number=15, bcm_pin=22, pin_name=""))
        print str(helper_gpio_create(pin_position=16, pin_number=16, bcm_pin=23, pin_name=""))
        print str(helper_gpio_create(pin_position=17, pin_number=None, bcm_pin=None, pin_name="3v3 Power"))
        print str(helper_gpio_create(pin_position=18, pin_number=18, bcm_pin=24, pin_name=""))
        print str(helper_gpio_create(pin_position=19, pin_number=19, bcm_pin=10, pin_name="MOSI"))
        print str(helper_gpio_create(pin_position=20, pin_number=None, bcm_pin=None, pin_name="Ground"))
        print str(helper_gpio_create(pin_position=21, pin_number=21, bcm_pin=9, pin_name="MISO"))
        print str(helper_gpio_create(pin_position=22, pin_number=22, bcm_pin=25, pin_name=""))
        print str(helper_gpio_create(pin_position=23, pin_number=23, bcm_pin=11, pin_name="SCLK"))
        print str(helper_gpio_create(pin_position=24, pin_number=24, bcm_pin=8, pin_name="CEO"))
        print str(helper_gpio_create(pin_position=25, pin_number=None, bcm_pin=None, pin_name="Ground"))
        print str(helper_gpio_create(pin_position=26, pin_number=26, bcm_pin=7, pin_name="CE1"))
        print str(helper_gpio_create(pin_position=27, pin_number=27, bcm_pin=0, pin_name="IS_SD"))
        print str(helper_gpio_create(pin_position=28, pin_number=28, bcm_pin=1, pin_name="ID_SC"))
        print str(helper_gpio_create(pin_position=29, pin_number=29, bcm_pin=5, pin_name=""))
        print str(helper_gpio_create(pin_position=30, pin_number=None, bcm_pin=None, pin_name="Ground"))
        print str(helper_gpio_create(pin_position=31, pin_number=31, bcm_pin=6, pin_name=""))
        print str(helper_gpio_create(pin_position=32, pin_number=32, bcm_pin=12, pin_name="PWM0"))
        print str(helper_gpio_create(pin_position=33, pin_number=33, bcm_pin=13, pin_name="PWM1"))
        print str(helper_gpio_create(pin_position=34, pin_number=None, bcm_pin=None, pin_name="Ground"))
        print str(helper_gpio_create(pin_position=35, pin_number=35, bcm_pin=19, pin_name="MISO"))
        print str(helper_gpio_create(pin_position=36, pin_number=36, bcm_pin=16, pin_name=""))
        print str(helper_gpio_create(pin_position=37, pin_number=37, bcm_pin=26, pin_name=""))
        print str(helper_gpio_create(pin_position=38, pin_number=38, bcm_pin=20, pin_name="MOSI"))
        print str(helper_gpio_create(pin_position=39, pin_number=None, bcm_pin=None, pin_name="Ground"))
        print str(helper_gpio_create(pin_position=40, pin_number=40, bcm_pin=21, pin_name="SCLK"))


def helper_gpio_create(pin_position, pin_number, bcm_pin, pin_name=""):
    gpio_obj = GpioPin.query.filter_by(pin_position=pin_position).first()
    if gpio_obj is None:
        gpio_obj = GpioPin.create(pin_position=pin_position, pin_number=pin_number, bcm_pin=bcm_pin, pin_name=pin_name)
    return gpio_obj


def rasp_pi_data_setup():
    with app.app_context():
        from pipig.pi_gpio.raspberry_pi import PI_1_MODEL_A_PLUS, PI_1_MODEL_AB_REVISION_2, PI_1_MODEL_B_PLUS, PI_1_MODEL_B_REVISION_1, PI_2_MODEL_B, PI_MODEL_3, PI_MODEL_ZERO
        print str(helper_rasp_pi_data_setup(name=PI_1_MODEL_B_REVISION_1, pin_count=26))
        print str(helper_rasp_pi_data_setup(name=PI_1_MODEL_AB_REVISION_2, pin_count=26))
        print str(helper_rasp_pi_data_setup(name=PI_1_MODEL_B_PLUS, pin_count=40))
        print str(helper_rasp_pi_data_setup(name=PI_1_MODEL_A_PLUS, pin_count=40))
        print str(helper_rasp_pi_data_setup(name=PI_2_MODEL_B, pin_count=40))
        print str(helper_rasp_pi_data_setup(name=PI_MODEL_3, pin_count=40))
        print str(helper_rasp_pi_data_setup(name=PI_MODEL_ZERO, pin_count=40))


def helper_rasp_pi_data_setup(name, pin_count=40):
    pi_obj = RaspberryPi.query.filter_by(name=name).first()
    if pi_obj is None:
        pi_obj = RaspberryPi.create(name=name, pin_count=pin_count)
    return pi_obj

if __name__ == '__main__':
    gpio_data_setup()
    rasp_pi_data_setup()
