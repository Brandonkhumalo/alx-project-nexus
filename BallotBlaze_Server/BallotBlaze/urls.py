from django.urls import path
from .views.views import (
    PollListCreateView,
    PollRetrieveView,
    VoteView,
    PollResultsView,
    PaginatedPollListView,
    PollSearchView
)

urlpatterns = [
    path('polls/', PollListCreateView.as_view(), name='poll-list-create'),
    path('polls/<int:pk>/', PollRetrieveView.as_view(), name='poll-detail'),
    path('polls/vote/', VoteView.as_view(), name='poll-vote'),
    path('polls/<int:poll_id>/results/', PollResultsView.as_view(), name='poll-results'),
    path('polls/active/', PaginatedPollListView.as_view(), name='polls-active-paginated'),
    path('polls/search/', PollSearchView.as_view(), name='polls-search'),
]