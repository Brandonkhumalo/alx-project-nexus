from rest_framework import serializers
from ..models import Poll, PollOption, Vote

class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        fields = ['id', 'option_text', 'vote_count']

class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'created_at', 'expires_at', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data)
        for option in options_data:
            PollOption.objects.create(poll=poll, **option)
        return poll

class VoteSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    def validate(self, data):
        poll_id = data.get('poll_id')
        option_id = data.get('option_id')
        user = self.context['request'].user

        if Vote.objects.filter(user=user, poll_id=poll_id).exists():
            raise serializers.ValidationError("User has already voted in this poll.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        poll_id = validated_data['poll_id']
        option_id = validated_data['option_id']

        option = PollOption.objects.get(id=option_id, poll_id=poll_id)
        vote = Vote.objects.create(
            user=user,
            poll_id=poll_id,
            selected_option=option
        )
        # Update vote count
        option.vote_count += 1
        option.save()
        return vote