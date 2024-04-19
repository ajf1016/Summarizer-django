from django.urls import path
from api.v1.notes import views

urlpatterns = [
    path('get-all-notes/', views.view_all_notes),
    path('get-all-voices/', views.view_all_voices),
    path('get-single-voice/<int:pk>/', views.view_single_voice),
    path('get-single-note/<int:pk>/', views.view_single_note),
    path('upload-audio/', views.upload_audio),
]
