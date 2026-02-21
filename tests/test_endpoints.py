"""
Tests for FastAPI endpoints using Arrange-Act-Assert pattern
"""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities"""
    # Arrange
    expected_keys = {"Chess Club", "Programming Class", "Gym Class", 
                     "Basketball Team", "Tennis Club", "Drama Club", 
                     "Art Studio", "Debate Team", "Science Club"}
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert set(activities.keys()) == expected_keys
    assert all("description" in activity for activity in activities.values())
    assert all("schedule" in activity for activity in activities.values())
    assert all("max_participants" in activity for activity in activities.values())
    assert all("participants" in activity for activity in activities.values())


def test_signup_new_participant_successful(client):
    """Test that a new participant can successfully sign up for an activity"""
    # Arrange
    email = "newemail@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity in result["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_participant_fails(client):
    """Test that a participant already signed up cannot sign up again"""
    # Arrange
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "already signed up" in result["detail"].lower()


def test_unregister_participant_successful(client):
    """Test that a participant can successfully unregister from an activity"""
    # Arrange
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity = "Chess Club"
    
    # First verify they're signed up
    activities_before = client.get("/activities").json()
    assert email in activities_before[activity]["participants"]
    
    # Act
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert "Unregistered" in result["message"]
    
    # Verify participant was removed
    activities_after = client.get("/activities").json()
    assert email not in activities_after[activity]["participants"]


def test_unregister_non_participant_fails(client):
    """Test that unregistering a non-participant fails"""
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "not signed up" in result["detail"].lower()


def test_availability_updates_after_signup(client):
    """Test that spots available decreases after signup"""
    # Arrange
    activity = "Programming Class"
    email = "test@mergington.edu"
    
    # Get initial availability
    activities_before = client.get("/activities").json()
    max_participants_before = activities_before[activity]["max_participants"]
    participants_before = len(activities_before[activity]["participants"])
    spots_before = max_participants_before - participants_before
    
    # Act - Sign up
    client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    activities_after = client.get("/activities").json()
    participants_after = len(activities_after[activity]["participants"])
    spots_after = max_participants_before - participants_after
    
    assert spots_after == spots_before - 1
    assert participants_after == participants_before + 1
