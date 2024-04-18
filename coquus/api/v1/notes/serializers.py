from rest_framework.serializers import ModelSerializer
from notes.models import Note
from rest_framework import serializers


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ("id", "name", "audio",
                  "text",
                  "summary",
                  "is_deleted",
                  "created_at")
