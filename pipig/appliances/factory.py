from appliances.appliance import BasicAppliance
from appliances.models import Appliance, ApplianceType

APPLIANCE_TYPE_NAME_BASIC = 'Basic Appliance'

class FactoryAppliance:

    def build_object(self, appliance_id):

        db_obj = Appliance.query.filter_by(id=appliance_id).first()
        appliance_type_id = db_obj.get_type_id()
        appliance_type = ApplianceType.get(appliance_type_id)

        type_name = appliance_type.get_type()
        if type_name == APPLIANCE_TYPE_NAME_BASIC:
            return BasicAppliance(appliance_id)


        else:
            return None



