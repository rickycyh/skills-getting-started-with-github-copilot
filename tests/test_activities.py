from copy import deepcopy

import pytest


def test_list_activities(client, activity_data):
    # Arrange
    expected = deepcopy(activity_data)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected
    assert response.json()["Art Club"]["participants"] == []


@pytest.mark.parametrize("activity_name", ["Chess Club", "Art Club"])
def test_signup_adds_only_selected_participant(client, activity_data, activity_name):
    # Arrange
    email = "new+student@mergington.edu"
    expected = deepcopy(activity_data)
    expected[activity_name]["participants"].append(email)

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    listing = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert activity_data == expected
    assert listing.status_code == 200
    assert listing.json() == expected
    assert listing.json()[activity_name]["participants"].count(email) == 1


@pytest.mark.parametrize(
    "activity_name, email, status, detail",
    [
        ("Chess Club", "michael@mergington.edu", 400,
         "Student already signed up for this activity"),
        ("Unknown", "new@mergington.edu", 404, "Activity not found"),
    ],
)
def test_signup_rejects_invalid_registration(
    client, activity_data, activity_name, email, status, detail
):
    # Arrange
    original = deepcopy(activity_data)

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == status
    assert response.json() == {"detail": detail}
    assert activity_data == original


def test_unregister_removes_only_selected_participant(client, activity_data):
    # Arrange
    email = "michael@mergington.edu"
    expected = deepcopy(activity_data)
    expected["Chess Club"]["participants"].remove(email)

    # Act
    response = client.delete(
        "/activities/Chess Club/signup", params={"email": email}
    )
    listing = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from Chess Club"
    }
    assert activity_data == expected
    assert listing.status_code == 200
    assert listing.json() == expected


@pytest.mark.parametrize(
    "activity_name, email, detail",
    [
        ("Unknown", "michael@mergington.edu", "Activity not found"),
        ("Chess Club", "unknown@example.com",
         "Student is not signed up for this activity"),
        ("Art Club", "unknown@example.com",
         "Student is not signed up for this activity"),
    ],
)
def test_unregister_rejects_missing_registration(
    client, activity_data, activity_name, email, detail
):
    # Arrange
    original = deepcopy(activity_data)

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": detail}
    assert activity_data == original


@pytest.mark.parametrize("method", ["POST", "DELETE"])
def test_registration_requires_email(client, activity_data, method):
    # Arrange
    original = deepcopy(activity_data)

    # Act
    response = client.request(method, "/activities/Chess Club/signup")

    # Assert
    assert response.status_code == 422
    assert any(
        error["loc"] == ["query", "email"] and error["type"] == "missing"
        for error in response.json()["detail"]
    )
    assert activity_data == original


def test_registration_lifecycle(client, activity_data):
    # Arrange
    email = "new+student@mergington.edu"
    params = {"email": email}
    url = "/activities/Art Club/signup"
    original = deepcopy(activity_data)
    registered = deepcopy(original)
    registered["Art Club"]["participants"].append(email)

    # Act
    signup = client.post(url, params=params)
    after_signup = client.get("/activities")
    duplicate_signup = client.post(url, params=params)
    unregister = client.delete(url, params=params)
    after_unregister = client.get("/activities")
    repeated_unregister = client.delete(url, params=params)
    signup_again = client.post(url, params=params)
    after_signup_again = client.get("/activities")

    # Assert
    assert signup.status_code == 200
    assert signup.json() == {"message": f"Signed up {email} for Art Club"}
    assert after_signup.status_code == 200
    assert after_signup.json() == registered
    assert duplicate_signup.status_code == 400
    assert duplicate_signup.json() == {
        "detail": "Student already signed up for this activity"
    }
    assert unregister.status_code == 200
    assert unregister.json() == {"message": f"Unregistered {email} from Art Club"}
    assert after_unregister.status_code == 200
    assert after_unregister.json() == original
    assert repeated_unregister.status_code == 404
    assert repeated_unregister.json() == {
        "detail": "Student is not signed up for this activity"
    }
    assert signup_again.status_code == 200
    assert signup_again.json() == {"message": f"Signed up {email} for Art Club"}
    assert after_signup_again.status_code == 200
    assert after_signup_again.json() == registered
    assert activity_data == registered
