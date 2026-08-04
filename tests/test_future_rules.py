import pytest


@pytest.mark.xfail(reason="Capacity rule is not implemented yet.", strict=False)
def test_signup_rejects_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    activities = client.get("/activities").json()
    max_participants = activities[activity_name]["max_participants"]

    for index in range(max_participants - len(activities[activity_name]["participants"])):
        email = f"fill-{index}@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": "overflow@mergington.edu"}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


@pytest.mark.xfail(reason="Email format validation is not implemented yet.", strict=False)
def test_signup_rejects_invalid_email_format(client):
    # Arrange
    activity_name = "Chess Club"
    invalid_email = "invalid-email-format"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": invalid_email})

    # Assert
    assert response.status_code == 422
