from pipig.models import PiPig

def configure_pipig(data):
    session_name = data.get('session name')
    recipe_id = data.get('recipe id')
    raspberry_pi_id = data.get('raspberry pi id')

    pipig = PiPig.create(recipe_id=recipe_id, pi_id=raspberry_pi_id, session_name=session_name)

    return pipig

