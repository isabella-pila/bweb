import pytest
from petfit.domain.entities.user import User
from petfit.domain.entities.recipe import Recipe
#from petfit.domain.entities.comment import Comment
from petfit.domain.value_objects.email_vo import Email
from petfit.domain.value_objects.password import Password


def test_create_user():
    email = Email("user@example.com")
    pwd = Password("Secret@123")
    user = User("1", "User", email, pwd)
    assert user.id == "1"


def test_create_user2():
    email = Email("user@example.com")
    pwd = Password("Secret@123")
    user = User("1", "User", email, pwd)
    assert user.email == "user@example.com"


def test_invalid_email():
    with pytest.raises(ValueError):
        User("1", "User", Email("usercom"), Password("Secret@123"))


def test_create_recipe():
    recipe = Recipe("1", "Title", "Ovo, leite, açúcar", "Misture tudo e ponha no forno", "true")
    assert recipe.title == "Title"


'''def test_create_comment():
    comment = Comment("1", "post1", "user1", "Nice post!", "2024-01-01")
    assert comment.comment == "Nice post!"'''