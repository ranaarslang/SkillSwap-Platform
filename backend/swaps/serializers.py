from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message, Profile, Review, Session

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"

class SessionSerializer(serializers.ModelSerializer):
    requester = UserSerializer(read_only=True)
    partner = UserSerializer(read_only=True)
    class Meta:
        model = Session
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["reviewer"]
        extra_kwargs = {"rating": {"min_value": 1, "max_value": 5}}
