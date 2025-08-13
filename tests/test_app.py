import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        # Updated tests to match original HTML structure
        assert '<header class="navbar' in html
        assert '<div class="profile">' in html
        assert '<section id="about"' in html
        assert 'id="education"' in html
        assert 'id="experience-section"' in html
        assert 'id="map"' in html

    def test_timeline(self):
        # Initially there should be 0 posts
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        assert isinstance(json_data, list)
        assert len(json_data) == 0

        # Create a new post (valid)
        response = self.client.post("/api/timeline_post", data={
            "name": "Test User",
            "email": "test@example.com",
            "content": "This is a test post."
        })
        assert response.status_code == 201
        post = response.get_json()
        assert post["name"] == "Test User"
        assert post["email"] == "test@example.com"
        assert post["content"] == "This is a test post."

        # Check that the post is returned in GET
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        json_data = response.get_json()
        assert len(json_data) == 1
        assert json_data[0]["name"] == "Test User"
        assert json_data[0]["email"] == "test@example.com"
        assert json_data[0]["content"] == "This is a test post."

        # POST with missing fields
        response = self.client.post("/api/timeline_post", data={
            "name": "Incomplete User",
            "email": "",
            "content": "Missing email"
        })
        assert response.status_code == 400
        assert "error" in response.get_json()

        response = self.client.post("/api/timeline_post", data={
            "name": "",
            "email": "test@example.com",
            "content": "Missing name"
        })
        assert response.status_code == 400
        assert "error" in response.get_json()

        response = self.client.post("/api/timeline_post", data={
            "name": "Test",
            "email": "test@example.com",
            "content": ""
        })
        assert response.status_code == 400
        assert "error" in response.get_json()
        
    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data=
        {"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data=
        {"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data=
        {"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
