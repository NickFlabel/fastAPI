import pytest
from jose import jwt
from app.config import settings
from app import schemas


def test_create_user(client):
    data = {
        "email": "test@test.com",
        "password": "test123"
    }
    res = client.post("/users/", json=data)
    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == "test@test.com"


def test_login_user(client, session, test_user):
    data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    res = client.post("/login", data=data)
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORYTHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'test123', 403),
    ('test2@test.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', "wrongpassword", 403),
    (None, "test123", 422),
    ("test2@gmail.com", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={
        "username": email,
        "password": password
    })

    assert res.status_code == status_code