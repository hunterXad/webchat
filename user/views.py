from django.shortcuts import render, redirect , get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm , ChatRoomForm , ProfileForm
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message ,Profile
from django.utils import timezone


# Create your views here.
# Home page
def index(request):
    return render(request, 'index.html')

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Ensure correct redirection to the login page
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profilechange(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profilechange')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profilechange.html', {'form': form, 'user': request.user})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'user': request.user})




@login_required
def chat_rooms(request):
    rooms = ChatRoom.objects.all()
    return render(request, 'chat_rooms.html', {'rooms': rooms})

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    messages = Message.objects.filter(room=room).order_by('timestamp')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(room=room, sender=request.user, content=content, timestamp=timezone.now())
            return redirect('chat_room', room_id=room.id)
    return render(request, 'chat_room.html', {'room': room, 'messages': messages})
# في ملف views.py



@login_required
def create_chat_room(request):
    if request.method == 'POST':
        form = ChatRoomForm(request.POST, request.FILES)  # أضف request.FILES هنا
        if form.is_valid():
            chat_room = form.save(commit=False)
            chat_room.created_by = request.user
            chat_room.created_at = timezone.now()
            chat_room.save()
            return redirect('chat_rooms')
    else:
        form = ChatRoomForm()
    return render(request, 'create_chat_room.html', {'form': form})

@login_required
def delete_chat_room(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    if chat_room.created_by == request.user:  # Check if current user is the creator
        chat_room.delete()
    return redirect('chat_rooms')
