from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app import activities, app


class UnregisterTests(TestCase):
    def setUp(self):
        state = patch.dict(activities, deepcopy(activities))
        state.start()
        self.addCleanup(state.stop)
        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    def test_unregister_removes_only_selected_participant(self):
        original = deepcopy(activities)
        response = self.client.delete(
            "/activities/Chess%20Club/signup",
            params={"email": "michael@mergington.edu"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"message": "Unregistered michael@mergington.edu from Chess Club"},
        )
        original["Chess Club"]["participants"].remove("michael@mergington.edu")
        self.assertEqual(self.client.get("/activities").json(), original)

    def test_unregister_unknown_activity(self):
        original = deepcopy(activities)
        response = self.client.delete(
            "/activities/Unknown/signup", params={"email": "michael@mergington.edu"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Activity not found"})
        self.assertEqual(activities, original)

    def test_unregister_unknown_participant(self):
        original = deepcopy(activities)
        response = self.client.delete(
            "/activities/Chess%20Club/signup", params={"email": "unknown@example.com"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(), {"detail": "Student is not signed up for this activity"}
        )
        self.assertEqual(activities, original)

    def test_unregister_requires_email(self):
        original = deepcopy(activities)
        response = self.client.delete("/activities/Chess%20Club/signup")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(activities, original)

    def test_participant_can_sign_up_again_after_unregistering(self):
        params = {"email": "new+student@mergington.edu"}
        url = "/activities/Chess%20Club/signup"
        self.assertEqual(self.client.post(url, params=params).status_code, 200)
        self.assertEqual(self.client.post(url, params=params).status_code, 400)
        self.assertEqual(self.client.delete(url, params=params).status_code, 200)
        self.assertEqual(self.client.delete(url, params=params).status_code, 404)
        self.assertEqual(self.client.post(url, params=params).status_code, 200)
        self.assertEqual(
            activities["Chess Club"]["participants"].count(params["email"]), 1
        )
