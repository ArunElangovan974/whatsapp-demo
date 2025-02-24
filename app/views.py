from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message


# Create your views here.


# User Registration
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# User Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to home after login
        else:
            messages.error(request, "Invalid credentials!")
    
    return render(request, 'login.html')

# User Logout
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def chat_view(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    messages = Message.objects.filter(
        sender=request.user, receiver=receiver
    ) | Message.objects.filter(
        sender=receiver, receiver=request.user
    )
    messages = messages.order_by('timestamp')

    if request.method == "POST":
        content = request.POST.get('content')  
        print("Received Message:", content)

        if content:
            Message.objects.create(sender=request.user, receiver=receiver, text=content)
        return redirect(f'/chat/{user_id}/')  

    return render(request, 'chat.html', {'receiver': receiver, 'messages': messages})