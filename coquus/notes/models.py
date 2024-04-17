from django.db import models


class VoiceNote(models.Model):
    name = models.CharField(max_length=255)
    voice_data = models.FileField(upload_to='voice/')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'voice_notes'
        verbose_name_plural = 'voice notes'

    def __str__(self):
        return self.name
