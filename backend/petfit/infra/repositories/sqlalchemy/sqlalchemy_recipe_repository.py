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

    async def get_all(self) -> List[Recipe]:
        result = await self._session.execute(
            select(RecipeModel).options(joinedload(RecipeModel.user_id))
        )
        return [recipe.to_entity() for recipe in result.unique().scalars().all()]

    async def get_by_id(self, recipe_id: str) -> Optional[Recipe]:
        result = await self._session.execute(
            select(RecipeModel)
            .options(joinedload(RecipeModel.user_id))
            .where(RecipeModel.id == recipe_id)
        )
        recipe = result.unique().scalar_one_or_none()
        return recipe.to_entity() if recipe else None

    async def create(self, recipe: Recipe) -> Recipe:
        db_recipe = RecipeModel.from_entity(recipe)
        self._session.add(db_recipe)
        await self._session.commit()
        await self._session.refresh(db_recipe)
        return db_recipe.to_entity()

    async def delete(self, recipe_id: str) -> None:
        await self._session.execute(delete(RecipeModel).where(RecipeModel.id == recipe_id))
        await self._session.commit()