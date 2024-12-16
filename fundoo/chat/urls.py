from django.urls import re_path
from . import views

urlpatterns = [
    # URL pattern for chatting
    re_path(r'^chat/$', views.chatting, name='chatting'),

    # URL pattern for the room, passing room_name as a parameter
    re_path(r'^room/(?P<room_name>\w+)/$', views.room, name='room'),

    # URL pattern for messages, using room_name as a parameter
    re_path(r'^message/(?P<room_name>\w+)/$', views.message, name='message'),

    # URL pattern for logout
    re_path(r'^logout/$', views.logout_u, name='logout'),
]
