from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Event, Registration
from django.contrib.auth.decorators import login_required

# 1. Admin Dashboard (See all events)
def admin_dashboard(request):
    events = Event.objects.all()
    return render(request, 'admin_portal/dashboard.html', {'events': events})

# 2. Create Event View
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description')
        date = request.POST.get('date')
        location = request.POST.get('location')
        
        # New Fields
        contact = request.POST.get('contact_number')
        organizer = request.POST.get('organizer_name')
        capacity = request.POST.get('capacity')
        
        # IMAGE HANDLING
        banner = request.FILES.get('banner') # Get the file object
        
        Event.objects.create(
            title=title, 
            description=desc, 
            date=date, 
            location=location,
            contact_number=contact,
            organizer_name=organizer,
            capacity=capacity,
            banner=banner
        )
        return redirect('admin_dashboard')
        
    return render(request, 'admin_portal/create_event.html')

# 3. View Participants for a specific event
def event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Get all students registered for this event
    registrations = Registration.objects.filter(event=event).select_related('student')
    
    return render(request, 'admin_portal/participants.html', {
        'event': event, 
        'regs': registrations
    })

def delete_event(request, event_id):
    # Security: Ensure only staff can delete
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to delete events.")
        return redirect('event_feed')

    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, f"Event '{event.title}' has been deleted.")
        return redirect('admin_dashboard')
    
    # If someone tries to access via GET, just send them back
    return redirect('admin_dashboard')