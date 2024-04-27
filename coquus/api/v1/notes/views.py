import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.v1.notes.serializers import NoteSerializer, AudioSerializer
from notes.models import Note, Audio
import whisper
import google.generativeai as genai
from django.http import JsonResponse, FileResponse
from django.conf import settings
from dotenv import load_dotenv
import asyncio
load_dotenv()

GOOGLE_API_KEY = os.getenv('GEMINI_KEY')
genai.configure(api_key=GOOGLE_API_KEY)


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
    data = request.data
    serializer = AudioSerializer(data=data, context=context)
    if serializer.is_valid():
        audio_instance = serializer.save()
        response_data = {
            'status_code': 6000,
            'message': 'Audio uploaded successfully',
            'data': AudioSerializer(audio_instance, context=context).data
        }
        return Response(response_data)

    response_data = {
        'status_code': 6001,
        'message': 'Audio uploading is failed',
        'data': serializer.errors,
    }
    return Response(response_data)


# for converting audio to text and summarize
@api_view(['GET'])
@permission_classes([AllowAny])
def convert_audio_to_text_and_summarize(request, pk):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    context = {
        "request": request
    }

    if Audio.objects.filter(pk=pk).exists():
        instance = Audio.objects.get(pk=pk)
        serializer = AudioSerializer(instance, context=context)
        audio_file = instance.audio_file
        audio_response = FileResponse(audio_file, content_type='audio/mpeg')
        audio_response['Content-Disposition'] = f'attachment; filename="{
            audio_file.name}"'

        async def get_text():
            return await audioToText(audio_file.path)
        raw_text = loop.run_until_complete(get_text())

        print("WHISPER TEXT", raw_text)

        async def get_summary():
            return await summarize(raw_text)
        summarized_text = loop.run_until_complete(get_summary())
        print("SUMMARY TEXT", summarized_text)

        note = Note.objects.create(
            text=raw_text,
            summary=summarized_text,
            audio=serializer.instance
        )

        response_data = {
            'status_code': 6000,
            'message': 'Audio converted to text',
            'data': NoteSerializer(note).data,
        }
        return Response(response_data)
    else:
        response_data = {
            'status_code': 6001,
            'message': 'Audio not found',
        }
        return JsonResponse(response_data)


# audio to text conversion(Whisper ai)
async def audioToText(audio_file):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print("AUdio TEXT 1", type(audio_file))
    model = whisper.load_model("base")

    print("AUdio TEXT 2", audio_file)
    raw_text = model.transcribe(audio_file, language="tibetan")
    print("AUdio TEXT 3")

    return raw_text["text"]


# summarize text(Gemini ai)
async def summarize(raw_text):
    model = genai.GenerativeModel('gemini-pro')
    summarized_text = model.generate_content("Summarize this text" + raw_text)

    return summarized_text.text
