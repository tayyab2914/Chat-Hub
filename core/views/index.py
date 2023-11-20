from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from ..models import UserProfile
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'pages/landing.html')

@login_required(login_url='/signin')
def dashboard(request):
    return render(request, 'pages/dashboard.html')

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
    
