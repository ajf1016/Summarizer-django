from rest_framework.serializers import ModelSerializer
from notes.models import VoiceNote
from rest_framework import serializers


class NoteSerializer(ModelSerializer):
    class Meta:
        model = VoiceNote
        fields = ("id", "name", "voice_data", "is_deleted")
