import pytest
from blog.domain.values_objects.email_vo import Email
from blog.domain.values_objects.password import Password
from blog.domain.entities.user import User


def test_create_user():
    email = Email("user@example.com")
    pwd = Password("Secret123")
    user = User("1",'User',email,pwd,"user")
    assert user.name == "Test User"


