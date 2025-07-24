# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html

        # Additional homepage checks
        assert "Software Development Intern" in html
        assert "University of California: Santa Cruz" in html
        assert "Urban Photography" in html

    def test_timeline(self):
        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert 'timeline_posts' in json
        assert len(json["timeline_posts"]) == 0

        # POST a valid timeline post
        post_response = self.client.post('/api/timeline_post', data={
            "name": "Test Code",
            "email": "test@test.com",
            "content": "Testing!"
        })
        assert post_response.status_code == 200
        json = post_response.get_json()
        assert json["name"] == "Test Code"
        assert json["email"] == "test@test.com"
        assert json["content"] == "Testing!"

        # Confirm the post appears in GET response
        get_response = self.client.get('/api/timeline_post')
        data = get_response.get_json()
        assert len(data["timeline_posts"]) == 1
        assert data["timeline_posts"][0]["name"] == "Test Code"

        # Confirm the post appears on the timeline page
        page_response = self.client.get('/timeline')
        assert page_response.status_code == 200
        page_html = page_response.get_data(as_text=True)
        assert "Test Code" in page_html
        assert "Testing!" in page_html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post('/api/timeline_post', data={
            "email": "john@example.com",
            "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post('/api/timeline_post', data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": ""
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post('/api/timeline_post', data={
            "name": "John Doe",
            "email": "not-an-email",
            "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
