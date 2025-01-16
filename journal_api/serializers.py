from rest_framework import serializers
from django.contrib.auth.models import User
from .models import JournalEntry


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = [
            "id",
            "date",
            "content",
            "concepts_learned",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["date", "created_at", "updated_at"]
