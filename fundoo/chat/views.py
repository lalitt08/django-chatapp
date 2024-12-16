from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def chatting(request):
    return render(request, 'chat.html', {})

def room(request, room_name):
    # Passing room name to the template
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def message(request, room_name):
    # This view will handle the message view.
    # For now, we're just rendering the room again or can process messages here
    return render(request, 'message.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def logout_u(request):
    # Handle logout or just render the login page
    return render(request, 'login.html', {})
