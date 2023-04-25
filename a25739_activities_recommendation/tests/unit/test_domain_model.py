from datetime import date



import pytest

class User():
    """Create user table"""


    def __init__(self, username, password):
        self.username = username
        self.password = password


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')

def test_user(user):
    assert user.username == 'dbowie'


