from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    # Basic Info
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    
    # NEW FIELDS
    # Requires 'Pillow' library: pip install Pillow
    banner = models.ImageField(upload_to='event_banners/', blank=True, null=True) 
    
    contact_number = models.CharField(max_length=15, help_text="Contact number for queries")
    organizer_name = models.CharField(max_length=100, default="Student Council")
    
    # Optional: Limit participants
    capacity = models.IntegerField(default=100, help_text="Max number of students allowed")
    
    def __str__(self):
        return self.title

class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.event.title}"