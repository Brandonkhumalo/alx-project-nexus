from django.test import TestCase
from BallotBlaze.models import Poll, PollOption
from django.utils import timezone
from datetime import timedelta

class PollModelTest(TestCase):
    def test_poll_creation(self):
        poll = Poll.objects.create(
            title="Best programming language?",
            expires_at=timezone.now() + timedelta(days=1)
        )
        self.assertEqual(str(poll), poll.title)