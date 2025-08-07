from django.urls import path
from .views.views import (
    PollListCreateView,
    PollRetrieveView,
    VoteView,
    PollResultsView,
    PaginatedPollListView,
    PollSearchView,
)

from .views import auth

urlpatterns = [
    path('create/poll/', PollListCreateView.as_view(), name='poll-list-create'),
    path('polls/<int:pk>/', PollRetrieveView.as_view(), name='poll-detail'),
    path('polls/vote/', VoteView.as_view(), name='poll-vote'),
    path('polls/<int:poll_id>/results/', PollResultsView.as_view(), name='poll-results'),
    path('polls/active/', PaginatedPollListView.as_view(), name='polls-active-paginated'),
    path('polls/search/', PollSearchView.as_view(), name='polls-search'),

    path('user/registration/', auth.signup, name='signup'),
    path('user/login/', auth.login, name='login'),
    path('user/log_out/', auth.logout, name='logout'),
]