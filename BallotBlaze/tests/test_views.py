from rest_framework.test import APITestCase
from BallotBlaze.models import Poll, PollOption
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()

class VoteViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass123")
        self.client.force_authenticate(user=self.user)

        self.poll = Poll.objects.create(
            title="Favorite framework?",
            expires_at=timezone.now() + timedelta(days=1)
        )
        self.option = PollOption.objects.create(poll=self.poll, option_text="Django")

    def test_cast_vote(self):
        url = reverse("poll-vote")
        data = {
            "poll_id": self.poll.id,
            "option_id": self.option.id
        }
        response = self.client.post(url, data, format="json")
        print("Response:", response.status_code, response.data)
        self.assertEqual(response.status_code, 201)
