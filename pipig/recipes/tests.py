from test_helpers.test_base import BaseTestCase
from pipig.recipes.models import Recipe

#________________________________________________________________
#
# Unit Tests
#________________________________________________________________

class RecipesModelTests(BaseTestCase):
    def test_session_name(self):
        recipe = Recipe.create(name="Name")
        self.assertTrue(recipe.get_name() == "Name")

#________________________________________________________________
#
# Builders to use in Unit Tests
#________________________________________________________________

def build_recipe_model(base_name):
    recipe = Recipe.create(name="%sRecipeModel" % base_name)
    return recipe