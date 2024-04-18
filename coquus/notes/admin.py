from django.contrib import admin
from notes.models import Note, Audio


class NoteAdmin(admin.ModelAdmin):
    list_display = ['get_audio_name', 'summary', 'created_at']

    def get_audio_name(self, obj):
        return obj.audio.name
    get_audio_name.short_description = 'Audio Name'


admin.site.register(Note, NoteAdmin)


class AudioAdmin(admin.ModelAdmin):
    list_display = ['name', 'audio_file', 'uploaded_at']
    model = Audio


admin.site.register(Audio, AudioAdmin)
