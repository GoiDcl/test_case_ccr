import pytest


@pytest.fixture
def super_user():
    from django.contrib.auth.backends import UserModel
    user_data = {
        'username': 'test_user',
        'email': '123@lol.com',
        'password': 'password',
    }
    user = UserModel._default_manager.create_superuser(**user_data)
    return user
