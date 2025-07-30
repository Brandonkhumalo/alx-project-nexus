from rest_framework import generics, status
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models import Poll, PollOption, Vote
from ..serializers.pollSerializer import PollSerializer, VoteSerializer, PollOptionSerializer
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework.filters import SearchFilter
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PollRetrieveView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class VoteView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = VoteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        poll = Poll.objects.get(id=serializer.validated_data['poll_id'])
        if poll.expires_at < now():
            return Response({'detail': 'This poll has expired.'}, status=400)

        vote = serializer.save()

        # Real-time result push
        options = PollOption.objects.filter(poll=poll)
        serialized = PollOptionSerializer(options, many=True).data

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'poll_{poll.id}',
            {
                'type': 'poll_update',
                'data': {
                    'poll': poll.title,
                    'results': serialized
                }
            }
        )

        return Response({'detail': 'Vote cast successfully.'}, status=status.HTTP_201_CREATED)


class PollResultsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return Response({'detail': 'Poll not found'}, status=404)

        options = PollOption.objects.filter(poll=poll)
        serializer = PollOptionSerializer(options, many=True)
        return Response({
            'poll': poll.title,
            'results': serializer.data
        })

class PollCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'  # newest polls first

class PaginatedPollListView(generics.ListAPIView):
    queryset = Poll.objects.filter(expires_at__gt=now())  # only active polls
    serializer_class = PollSerializer
    pagination_class = PollCursorPagination

class PollSearchView(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']  # search by title