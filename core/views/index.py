from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from ..models import UserProfile
from django.contrib.auth.decorators import login_required
from chat.models import Room
from chat.serializers import RoomSerializer

def index(request):
    return render(request, 'pages/landing.html')

@login_required(login_url='/signin')
def dashboard(request):
    rooms_obj = Room.objects.filter(admin=request.user)[:3]
    serializer = RoomSerializer(rooms_obj, many=True)
    room_list = [dict(item) for item in serializer.data]

    public_room_obj = Room.objects.filter(is_public=True)
    public_serializer = RoomSerializer(public_room_obj, many=True)
    public_room_list = [dict(item) for item in public_serializer.data]

    context = {'rooms':room_list, 'public_rooms':public_room_list}
    return render(request, 'pages/dashboard.html', context)

def edit_profile_pic(request):
    if request.method=="POST":
        uploaded_file = request.FILES.get('profile_picture')
        if uploaded_file:
            # Save the file to a specific location
            fs = FileSystemStorage()
            filename = fs.save(f"users/{request.user.username}/profile_pics/{uploaded_file.name}", uploaded_file)
            profile = UserProfile.objects.get(user=request.user)
            # Update the user's profile with the file path
            profile.profile_picture = filename
            profile.save()
        return redirect('/dashboard')
    
@login_required(login_url='/signin')
def comingsoon(request):
    return render(request, 'pages/comingsoon.html')
