from time import time

from pipig.appliances.models import Appliance
from pipig.binders.models import BindDatapointsAppliances, BindDatapointsSensors
from pipig.curing_sessions.models import CuringSession
from pipig.data_points.models import DataPoints, DataPoint
from pipig.recipes.models import Recipe
from pipig.sensors.models import Sensor

recipe = Recipe.create(name="InitRecipe")
session = CuringSession.create(name="InitCuringSession", start_time=time())
recipe_id = recipe.get_id()
session_id = session.get_id()

