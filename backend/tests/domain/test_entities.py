import pytest
from petfit.domain.entities.user import User
from petfit.domain.value_objects.email_vo import Email
from petfit.domain.value_objects.password import Password
from petfit.domain.entities.recipe import Recipe

def test_create_user():
    email = Email("user@example.com")
    pwd = Password("Secret123!")
    user = User("1", "User", email, pwd)
    assert user.id == "1"
    assert user.name == "User"
    assert user.email == email
    assert user.password == pwd

def test_recipe_creation_all_fields():
    recipe = Recipe(
        id="1",
        title="Bolo de Cenoura",
        ingredients="cenoura, ovos, farinha de aveia",
        instructions="Misture tudo e asse por 40 minutos.",
        img_url="http://exemplo.com/bolo.jpg",
        category="gato"
    )
    assert recipe.id == "1"
    assert recipe.title == "Bolo de Cenoura"
    assert recipe.ingredients == "cenoura, ovos, farinha de aveia"
    assert recipe.instructions == "Misture tudo e asse por 40 minutos."
    assert recipe.category == "gato"

