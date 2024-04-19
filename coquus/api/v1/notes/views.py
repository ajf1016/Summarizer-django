from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.v1.notes.serializers import NoteSerializer, AudioSerializer
from notes.models import Note, Audio


# for showing all notes
@api_view(['GET'])
@permission_classes([AllowAny])
def view_all_notes(request):
    if not Note.objects.filter(is_deleted=False).exists():
        response_data = {
            "status_code": 6001,
            "message": "No notes found"
        }
        return Response(response_data)

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
            "message": "Note not found"
        }
        return Response(response_data)


# for showing all voices
@api_view(['GET'])
@permission_classes([AllowAny])
def view_all_voices(request):
    instance = Audio.objects.filter(is_deleted=False)
    context = {
        "request": request
    }
    serializer = AudioSerializer(instance, many=True, context=context)

    response_data = {
        "status_code": 6000,
        "data": serializer.data
    }
    return Response(response_data)


# for showing single voice
@api_view(['GET'])
@permission_classes([AllowAny])
def view_single_voice(request, pk):
    if Audio.objects.filter(pk=pk).exists():
        instance = Audio.objects.get(pk=pk)
        context = {
            "request": request
        }
        serializer = AudioSerializer(instance, context=context)

        response_data = {
            "status_code": 6000,
            "data": serializer.data
        }
        return Response(response_data)
    else:
        response_data = {
            "status_code": 6001,
            "message": "Audio not found"
        }
        return Response(response_data)


# for uploading audio
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_audio(request):
    context = {
        "request": request
    }
    serializer = AudioSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            'status_code': 6000,
            'message': 'Audio uploaded successfully',
            'data': serializer.data,
        }
        return Response(response_data)

    response_data = {
        'status_code': 6001,
        'message': 'Audio uploading is failed',
        'data': serializer.errors,
    }
    return Response(response_data)
