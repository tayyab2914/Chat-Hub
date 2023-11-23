from django.shortcuts import render, redirect
from django.http import JsonResponse
from django_countries import countries
from restcountries import RestCountryApiV2 as rapi
import requests
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .serializers import *
from core.models import UserProfile
from django.contrib.auth.models import User
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@login_required(login_url='/signin')
def chat(request, key):
    try:
        rooms_obj = Room.objects.get(key=key)
        message_obj = Message.objects.filter(room=rooms_obj)
        room_serializer = RoomSerializer(rooms_obj)
        message_serializer = MessageSerializer(message_obj, many=True)
        messages_dict = [dict(item) for item in message_serializer.data]
        for message in messages_dict:
            user = User.objects.get(username=message['user'])
            user_profile = UserProfile.objects.get(user=user)
            message['profile_picture'] = user_profile.profile_picture.url
        context = {'room':room_serializer.data,'messages':messages_dict}
    except Exception as e:
        print(e)
        return redirect('/dashboard')
    return render(request,'pages/chat.html', context)

@login_required(login_url='/signin')
def created_rooms(request):
    rooms_obj = Room.objects.filter(admin=request.user)
    serializer = RoomSerializer(rooms_obj, many=True)
    simple_dicts_list = [dict(item) for item in serializer.data]
    context = simple_dicts_list
    context = {'rooms':context}
    return render(request,'pages/createdrooms.html', context)

@login_required(login_url='/signin')
def create(request):
    if request.method=="POST":
        roomname = request.POST.get('roomname')
        code = request.POST.get('code')
        ispublic = False if request.POST.get('ispublic') is None else True
        language = request.POST.get('language')
        room = Room.objects.create(admin=request.user, name=roomname, is_public=ispublic, language=language, country_code=code)
        return redirect(f"/chat/{room.key}")
    return render(request, 'pages/createroom.html')

@login_required(login_url='/signin')
def join(request):
    if request.method=='POST':
        key = request.POST.get('key')
        room = Room.objects.filter(key=key).exists()
        if room:
            return redirect(f"/chat/{key}")
        else:
            messages.error(request, "Room not found!")
    return render(request, 'pages/joinroom.html')

def language_list(request):
    language_data=[]
    for country in country_languages:
        url = f"https://restcountries.com/v3.1/alpha/{country_languages[country]['code']}"
        country_dict={'code':country_languages[country]['code'], 'language':country_languages[country]['language'], 'url':url}
        language_data.append(country_dict)
    return JsonResponse({'languages': language_data})

country_languages = {
    'United Kingdom': {'code': 'GB', 'language': 'English'},
    'Germany': {'code': 'DE', 'language': 'German'},
    'France': {'code': 'FR', 'language': 'French'},
    'Italy': {'code': 'IT', 'language': 'Italian'},
    'Spain': {'code': 'ES', 'language': 'Spanish'},
    'Japan': {'code': 'JP', 'language': 'Japanese'},
    'China': {'code': 'CN', 'language': 'Mandarin'},
    'India': {'code': 'IN', 'language': 'Hindi'},
    'Brazil': {'code': 'BR', 'language': 'Portuguese'},
    'Russia': {'code': 'RU', 'language': 'Russian'},
    'South Korea': {'code': 'KR', 'language': 'Korean'},
    'Turkey': {'code': 'TR', 'language': 'Turkish'},
    'Netherlands': {'code': 'NL', 'language': 'Dutch'},
    'Sweden': {'code': 'SE', 'language': 'Swedish'},
    'Denmark': {'code': 'DK', 'language': 'Danish'},
    'Norway': {'code': 'NO', 'language': 'Norwegian'},
    'Finland': {'code': 'FI', 'language': 'Finnish'},
    'Greece': {'code': 'GR', 'language': 'Greek'},
    'Vietnam': {'code': 'VN', 'language': 'Vietnamese'},
    'Thailand': {'code': 'TH', 'language': 'Thai'},
    'Indonesia': {'code': 'ID', 'language': 'Indonesian'},
    'Kenya': {'code': 'KE', 'language': 'Swahili'},
    'Philippines': {'code': 'PH', 'language': 'Tagalog'},
    'Pakistan': {'code': 'PK', 'language': 'Urdu'},
    # Add more countries and languages as needed
}

SYSTEM_ROLE = 'I will give you any language text and you have to convert into selected language. Your translation should be word by word translation and then full sentence translation.Also give messages with pronounciation and give instructions in english that this is word by word and this is full sentence'

client = OpenAI(api_key='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')

def get_translated_message(message, output_language):
    prompt = []
    prompt.append({"role": "system", "content": SYSTEM_ROLE})
    prompt.append({"role": "user", "content": f'Translate into {output_language}: {message}'})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt)
    reply = response.choices[0].message.content
    return reply

@csrf_exempt
def get_translated_text(request, key):
    data = json.loads(request.body.decode('utf-8'))
    room = Room.objects.get(key=key)
    #user = UserProfile.objects.get(user=request.user)
    message = data['message']
    reply = get_translated_message(message, room.language)
    #Message.objects.create(room=room,user=request.user,content=reply)

    return JsonResponse({'message':reply})