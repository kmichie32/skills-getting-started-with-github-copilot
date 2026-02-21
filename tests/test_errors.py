"""
Tests for error handling using Arrange-Act-Assert pattern
"""


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity returns 404"""
    # Arrange
    email = "test@mergington.edu"
    nonexistent_activity = "Underwater Basket Weaving"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "not found" in result["detail"].lower()


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregistering from a non-existent activity returns 404"""
    # Arrange
    email = "test@mergington.edu"
    nonexistent_activity = "Underwater Basket Weaving"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "not found" in result["detail"].lower()


def test_signup_with_url_encoded_activity_name(client):
    """Test that activity names with spaces are properly handled"""
    # Arrange
    email = "spacedactivity@mergington.edu"
    activity = "Programming Class"  # Has a space
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify the signup worked
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_response_structure_contains_required_fields(client):
    """Test that activity response contains all required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert set(activity_data.keys()) >= required_fields, \
            f"Activity {activity_name} missing required fields"
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["description"], str)
