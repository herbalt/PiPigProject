from pipig.pi_pig.models import PiPigModel
# from pipig.api.pi_pig.endpoints import pipig_instance


def configure_pipig(data):
    global pipig_instance
    session_name = data.get('session name')
    recipe_id = data.get('recipe id')
    raspberry_pi_id = data.get('raspberry pi id')

    pipig = PiPigModel.create(recipe_id=recipe_id, pi_id=raspberry_pi_id, session_name=session_name)
    pipig_instance = pipig
    return pipig_instance

