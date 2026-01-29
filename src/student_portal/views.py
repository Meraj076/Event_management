from django.shortcuts import render, redirect, get_object_or_404
from admin_portal.models import Event, Registration
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import EmailSignupForm
from django.contrib.auth.models import User
from admin_portal.models import Event, Registration

def custom_login(request):
    if request.method == 'POST':
        # 1. Get Email and Password
        email = request.POST.get('email')
        password = request.POST.get('password')
        login_type = request.POST.get('login_type')

        try:
            # 2. Find the user with this email
            user_obj = User.objects.get(email=email)
            
            # 3. Authenticate using the FOUND username and provided password
            user = authenticate(username=user_obj.username, password=password)

            if user is not None:
                # --- STRICT ROLE CHECKING (Same as before) ---
                if login_type == 'admin' and not user.is_staff:
                    messages.error(request, "Access Denied: You do not have Organizer privileges.")
                elif login_type == 'student' and user.is_staff:
                    messages.error(request, "Organizer accounts must log in using the Organizer toggle.")
                else:
                    login(request, user)
                    if login_type == 'admin':
                        return redirect('admin_dashboard')
                    else:
                        return redirect('event_feed')
            else:
                messages.error(request, "Invalid email or password.")

        except User.DoesNotExist:
            messages.error(request, "This email is not registered.")
            
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        # Get data directly from the input names in your HTML
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 1. Check Passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # 2. Check if Username/Email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'signup.html')

        # 3. Create User
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            # 4. Login and Redirect
            login(request, user)
            return redirect('event_feed')
            
        except Exception as e:
            messages.error(request, "An error occurred during signup.")
            print(e) # For debugging in terminal
            
    return render(request, 'signup.html')

def landing_page(request):
    return render(request, 'landing.html')

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check registration status
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(student=request.user, event=event).exists()

    return render(request, 'student_portal/event_detail.html', {
        'event': event,
        'is_registered': is_registered
    })

# 1. Student Home (List of Events)
def event_feed(request):
    events = Event.objects.all()
    return render(request, 'student_portal/feed.html', {'events': events})

# 2. Register Logic
@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if already registered to prevent duplicates
    if not Registration.objects.filter(student=request.user, event=event).exists():
        Registration.objects.create(student=request.user, event=event)
    
    # Redirect immediately to dashboard
    return redirect('my_registrations')

# 3. My Registrations (Status Check)
@login_required
def my_registrations(request):
    my_regs = Registration.objects.filter(student=request.user)
    return render(request, 'student_portal/my_regs.html', {'regs': my_regs})