from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.v1.notes.serializers import NoteSerializer
from notes.models import Note


# for showing all notes
@api_view(['GET'])
@permission_classes([AllowAny])
def view_all_notes(request):
    instance = Note.objects.filter(is_deleted=False)
    context = {
        "request": request
    }
    serializer = NoteSerializer(instance, many=True, context=context)

    response_data = {
        "status_code": 6000,
        "data": serializer.data
    }
    return Response(response_data)


# for showing single note
@api_view(['GET'])
@permission_classes([AllowAny])
def view_single_note(request, pk):
    if Note.objects.filter(pk=pk).exists():
        instance = Note.objects.get(pk=pk)
        context = {
            "request": request
        }
        serializer = NoteSerializer(instance, context=context)

        response_data = {
            "status_code": 6000,
            "data": serializer.data
        }
        return Response(response_data)
    else:
        response_data = {
            "status_code": 6001,
            "message": "Place not found"
        }
        return Response(response_data)


# for showing all voices
@api_view(['GET'])
@permission_classes([AllowAny])
def view_all_voices(request):
    pass


# for showing single voice
@api_view(['GET'])
@permission_classes([AllowAny])
def view_single_voice(request, pk):
    pass


# for uploading audio
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_audio(request, pk):
    pass
