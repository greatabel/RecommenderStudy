import pytest

from flask import session


def test_recommend(client):

    # Check that we can retrieve the articles page.
    data = {
    'activity':1,
    'activity_name': 'test activity name',
    'rtext': 'test',
    'rating':5
    }
    response = client.post('/recommend', data=data)
    assert response.status_code == 404



def test_login_without_auth(client):
    # Check that we can retrieve the articles page.
    response = client.post('/login')
    assert response.status_code == 404


def test_logout_without_auth(client):
    # Check that we can retrieve the articles page.
    response = client.post('/logout')
    assert response.status_code == 404


def test_register_without_auth(client):
    # Check that we can retrieve the articles page.
    response = client.post('/register')
    assert response.status_code == 404


