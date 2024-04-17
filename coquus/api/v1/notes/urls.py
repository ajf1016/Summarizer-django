from django.urls import path
from api.v1.notes import views

urlpatterns = [
    path('', views.view_all_notes),
    path('view-single-note/<int:pk>', views.view_single_note),
    path('api/v1/notes/upload-audio/', views.upload_audio, name='upload_audio'),
    # path('protected/<int:pk>', views.protected_place),
]
