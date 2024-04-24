from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from notes.models import Note, Audio
from rest_framework import serializers


class AudioSerializer(ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'


class NoteSerializer(ModelSerializer):
    audio = PrimaryKeyRelatedField(queryset=Audio.objects.all())
    audio_details = AudioSerializer(
        source='audio', read_only=True)

    class Meta:
        model = Note
        fields = ("id", "text", "summary", "created_at",
                  "is_deleted", "audio", "audio_details")
