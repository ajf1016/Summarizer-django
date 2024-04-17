from django.contrib import admin
from notes.models import VoiceNote


class VoiceNoteAdmin(admin.ModelAdmin):
    list_display = ['name', 'voice_data']
    model = VoiceNote


admin.site.register(VoiceNote, VoiceNoteAdmin)
