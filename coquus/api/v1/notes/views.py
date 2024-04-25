import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.v1.notes.serializers import NoteSerializer, AudioSerializer
from notes.models import Note, Audio
import whisper
import ssl
import google.generativeai as genai
from django.http import JsonResponse, FileResponse
from django.conf import settings
from dotenv import load_dotenv
import asyncio
import numpy as np
load_dotenv()

# ESP FILE PATH : coquus_audio_files/
# .env variables


GOOGLE_API_KEY = os.getenv('GEMINI_KEY')
# ssl._create_default_https_context = ssl._create_unverified_context
genai.configure(api_key=GOOGLE_API_KEY)

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
        # response_data = {
        #     'status_code': 6000,
        #     'message': 'Audio uploaded successfully',
        #     'data': serializer.data,
        # }

        audio = serializer.instance.audio_file
        # raw_text = audioToText(audio_file):
        print()

        summarized_text = ""

        # note_data = {
        #     'text': raw_text,
        #     'summary': summarized_text,
        #     'audio': serializer.instance
        # }
        # note = Note.objects.create(
        #     text=raw_text,
        #     summary=summarized_text,
        #     audio=serializer.instance
        # )

        response_data = {
            'status_code': 6000,
            'message': 'Audio uploaded successfully, note created',
            # 'data': NoteSerializer(note).data,
            'data': 'Audio converted'
        }
        return Response(response_data)

    response_data = {
        'status_code': 6001,
        'message': 'Audio uploading is failed',
        'data': serializer.errors,
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def audio_to_text(request, pk):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if Audio.objects.filter(pk=pk).exists():
        instance = Audio.objects.get(pk=pk)
        audio_file = instance.audio_file

        audio_response = FileResponse(audio_file, content_type='audio/mpeg')
        audio_response['Content-Disposition'] = f'attachment; filename="{
            audio_file.name}"'
        response_data = {
            'status_code': 6000,
            'message': 'Audio converted to text',
            'data': audio_file,
        }

        async def get_text():
            return await audioToText(audio_response)
        text = loop.run_until_complete(get_text())
        # return Response(response_data)
        return text
        # return audio_response
        # return Response(audio_file.name)
        # return FileResponse(audio_file, content_type='audio/mpeg')
    response_data = {
        'status_code': 6001,
        'message': 'Audio not found',
    }
    return JsonResponse(response_data)


# whisper function and gemini
async def audioToText(audio_file):
    await asyncio.sleep(5)
    print("AUdio TEXT 1", type(audio_file))
    model = whisper.load_model("base")

    print("AUdio TEXT 2", audio_file)
    text = model.transcribe(audio_file)
    print("AUdio TEXT 3")
    return text["text"]


def summarize(text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Summarize this text" + text)

    return response


r_text01 = " Thank you, Mr. Secretary General. Your excellencies, ladies and gentlemen, and distinguished guests. I'm honored to be here today. I stand before you, not as an expert, but as a concerned citizen. One of the 400,000 people who marched in the streets of New York on Sunday and the billions of others around the world who want to solve our climate crisis. As an actor, I pretend for a living. I play fictitious characters, often solving fictitious problems. I believe that mankind has looked at climate change in that same way, as if it were a fiction. As if pretending that climate change wasn't real would somehow make it go away. But I think we all know better than that now. Every week we're seeing new and undeniable climate events, evidence that accelerated climate change is here right now. Droughts are intensifying. Our oceans are acidifying with methane plumes rising up from the ocean floor. We are seeing extreme weather events and the West Antarctic and Greenland ice sheets melting at unprecedented rates decades ahead of scientific projections. None of this is rhetoric and none of it is hysteria. It is fact. The scientific community knows it, industry knows it, governments know it, even the United States military knows it. The Chief of the US Navy's Pacific Command Admiral Samuel Lockley recently said that climate change is our single greatest security threat. My friends, this body, perhaps more than any other gathering in human history now faces this difficult but achievable task. You can make history or you will be vilified by it. To be clear, this is not about just telling people to change their light bulbs or to buy a hybrid car. This disaster has grown beyond the choices that individuals make. This is now about our industries and our governments around the world taking decisive large-scale action. Now must be our moment for action. We need to put a price tag on carbon emissions and eliminate government subsidies for oil, coal and gas companies. We need to end the free ride that industrial polluters have been given in the name of a free market economy. They do not deserve our tax dollars. They deserve our scrutiny for the economy itself will die if our ecosystems collapse. The good news is that renewable energy is not only achievable but good economic policy. This is not a partisan debate. It is a human one. Clean air and a livable climate are analiable human rights. And solving this crisis is not a question of politics. It is a question of our own survival. This is the most urgent of times and the most urgent of messages. Honour delegates, leaders of the world, I pretend for a living but you do not. The people made their voices heard on Sunday around the world and the momentum will not stop. But now it is your turn. The time to answer humankind's greatest challenge is now. We beg of you to face it with courage and honesty. Thank you."
s_text01 = "Actor Leonardo DiCaprio addresses the UN, emphasizing the urgency of addressing climate change and its impact on the planet. He calls for decisive action from industries and governments, including pricing carbon emissions, ending fossil fuel subsidies, and investing in renewable energy. DiCaprio highlights the severity of climate events and the scientific consensus on the crisis, arguing that clean air and a livable climate are fundamental human rights. He implores delegates to take courageous steps toward a sustainable future, warning that inaction will have dire consequences for humanity."

r_text02 = "Sport has the power to change the world. It has the power to inspire. It has the power to unite people in a way that little as does. It speaks to youth in a language they understood. Sport can create hope where once there was only despair."
s_text02 = "Sport has a transformative ability: it inspires, unites, and communicates with youth on their level. It brings hope and positivity in situations characterized by hopelessness and despair."

r_text03 = "Thank you for such a wonderful introduction. Great. I'm here today to talk about motivation. And I've learned in my few years on this earth that motivation is really the key to affecting change in anything that you do. You can put a paper that was written without any motivation, without any effort, and you can put a paper that was written with drive and passion next to each other. It's clear which one is the winner. Motivation is the underlying factor. I believe in everything that we do on a daily basis. If you don't have motivation in something that you do, then you really can't achieve what it is that you want to achieve. Everyone has motivation for things that they're passionate about. Things that interest you. Things that inspire you. And of course you'll have motivation if you play a sport, if you're in drama, if you're in band, you'll have motivation to accomplish that task. But the true test of finding motivation is if you can find it in something that doesn't interest you. Personally, I'm interested in sitting through town council meetings and reading the 404 page town of Barnsville budget. But others might not find so much paper so interesting. However, motivation can be found in everything that you do. I like to look at it in terms of finding motivation as just putting yourself in someone else's shoes. When you're questioning, why do I have to do this? Why do I have to put in the time? Why do I have to put in the effort? You can just look at what you're doing and say, this helps this person because. Where this person is going to appreciate my effort and my motivation on this task because. And I've always found that that appreciation that others have for the effort that you put in, that's what motivates me. The fact that someone's going to appreciate what I did. So when the teacher gives you a paper or something to do and you say, this is stupid, I have better things to do. I'd much rather go outside and throw a football, whatever it is. Look at it and say, this person is going to appreciate the work. This person put in the effort to create the assignment. Now they're going to see it and they're going to appreciate it. And I do that in every assignment that I'm given and everything that has ever brought before me. And that's always something that I think we need to go out and look at when we go out to tackle an issue. Filing papers. People might not find it interesting. But think about how much help you're doing to somebody else. Think about the responsibility that you're helping someone else fulfill. And that sort of help and appreciation motivates you. For me, fine dressing is something that I like to do every single day. And I don't just do it because I enjoy it. I do it because people appreciate it. People see that. I took the extra time to prepare myself for whatever it is that I'm doing. And they thank me for it. And that thanks that appreciation is truly what motivates me to go out and do whatever it is that has put before me. So I want to finish briefly. Like just by saying that motivation is so important in anything that you do. And without it, you really can't accomplish what you want. But with it, you have the passion to affect change. You have the passion to make a difference. And you really do have the passion to go out and change the way things are done and make a difference in anything that you want to do. Thank you for your time and your ears."
s_text03 = "Motivation is crucial for success in any endeavor. Even in mundane tasks, motivation can be found by considering how our actions benefit others. Focusing on the appreciation we receive for our efforts, rather than solely on personal interests, can drive us to complete tasks effectively. By embracing this perspective, we can cultivate passion and make a meaningful impact on the world."

r_text04 = "Thank you for such a wonderful introduction. Great. I'm here today to talk about motivation. And I've learned in my few years on this earth that motivation is really the key to affecting change in anything that you do. You can put a paper that was written without any motivation, without any effort, and you can put a paper that was written with drive and passion next to each other. It's clear which one is the winner. Motivation is the underlying factor. I believe in everything that we do on a daily basis. If you don't have motivation in something that you do, then you really can't achieve what it is that you want to achieve. Everyone has motivation for things that they're passionate about. Things that interest you. Things that inspire you. And of course you'll have motivation if you play a sport, if you're in drama, if you're in band, you'll have motivation to accomplish that task. But the true test of finding motivation is if you can find it in something that doesn't interest you. Personally, I'm interested in sitting through town council meetings and reading the 404 page town of Barnsville budget. But others might not find so much paper so interesting. However, motivation can be found in everything that you do. I like to look at it in terms of finding motivation as just putting yourself in someone else's shoes. When you're questioning, why do I have to do this? Why do I have to put in the time? Why do I have to put in the effort? You can just look at what you're doing and say, this helps this person because. Where this person is going to appreciate my effort and my motivation on this task because. And I've always found that that appreciation that others have for the effort that you put in, that's what motivates me. The fact that someone's going to appreciate what I did. So when the teacher gives you a paper or something to do and you say, this is stupid, I have better things to do. I'd much rather go outside and throw a football, whatever it is. Look at it and say, this person is going to appreciate the work. This person put in the effort to create the assignment. Now they're going to see it and they're going to appreciate it. And I do that in every assignment that I'm given and everything that has ever brought before me. And that's always something that I think we need to go out and look at when we go out to tackle an issue. Filing papers. People might not find it interesting. But think about how much help you're doing to somebody else. Think about the responsibility that you're helping someone else fulfill. And that sort of help and appreciation motivates you. For me, fine dressing is something that I like to do every single day. And I don't just do it because I enjoy it. I do it because people appreciate it. People see that. I took the extra time to prepare myself for whatever it is that I'm doing. And they thank me for it. And that thanks that appreciation is truly what motivates me to go out and do whatever it is that has put before me. So I want to finish briefly. Like just by saying that motivation is so important in anything that you do. And without it, you really can't accomplish what you want. But with it, you have the passion to affect change. You have the passion to make a difference. And you really do have the passion to go out and change the way things are done and make a difference in anything that you want to do. Thank you for your time and your ears."
s_text04 = "Motivation is crucial for accomplishing goals and driving change. Everyone has passions that motivate them, but finding motivation in less interesting tasks requires putting yourself in others' shoes and considering the impact of your efforts on them. Appreciation from others can serve as a powerful motivator, fostering a sense of purpose and driving individuals to excel in their endeavors."
