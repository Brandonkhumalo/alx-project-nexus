from django.test import SimpleTestCase
from django.urls import reverse, resolve
from BallotBlaze.views.views import PollListCreateView

class UrlsTest(SimpleTestCase):
    def test_poll_list_url_resolves(self):
        url = reverse("poll-list-create")
        self.assertEqual(resolve(url).func.view_class, PollListCreateView)
