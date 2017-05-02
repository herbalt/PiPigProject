from pipig import app
from generics.models import GenericUnits


def data_setup():
    setup_generic_units()


def setup_generic_units():
    GenericUnits.query.delete()
    GenericUnits.create(code_name='COUNTER', display_units='')
    GenericUnits.create(code_name='CELCIUS', display_units='C')
    GenericUnits.create(code_name='FAHRENHEIT', display_units='F')
    GenericUnits.create(code_name='HUMIDITY', display_units='H')
    GenericUnits.create(code_name='NO UNITS', display_units='')
    return True


if __name__ == '__main__':
    with app.app_context():
        data_setup()