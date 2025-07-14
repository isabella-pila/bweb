from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from petfit.domain.entities.recipe import Recipe
from petfit.domain.repositories.recipe_repository import RecipeRepository
from petfit.infra.models.recipe_model import RecipeModel
from sqlalchemy.orm import joinedload


class SQLAlchemyRecipeRepository(RecipeRepository):
    def __init__(self, session: AsyncSession):
        self._session = session


    async def create(self, recipe: Recipe) -> Recipe:
        db_recipe = RecipeModel.from_entity(recipe)
        self._session.add(db_recipe)
        await self._session.commit()
        await self._session.refresh(db_recipe)
        return db_recipe.to_entity()

    async def delete(self, recipe_id: str) -> None:
        await self._session.execute(delete(RecipeModel).where(RecipeModel.id == recipe_id))
        await self._session.commit()