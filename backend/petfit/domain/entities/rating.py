from petfit.domain.entities.user import User
from petfit.domain.entities.recipe import Recipe

class  Rating:
    def __init__(self,id: str, user_id: User, recipe_id: Recipe, value: int):
        self.id = id
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.value = value