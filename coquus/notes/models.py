from django.db import models
import uuid


class Audio(models.Model):
    def generate_random_name():
        return str(uuid.uuid4())[:8]

    name = models.CharField(max_length=255, default=generate_random_name)
    audio_file = models.FileField(upload_to='voice/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Note(models.Model):
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE)
    text = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Note for {self.audio.name}"
