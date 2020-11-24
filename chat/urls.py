from django.urls import path, re_path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    ####
    path('view_chat_app', views.index),
    path('show_chat/<str:id>', views.show_chat_msg),
    path('add_message-json', views.add_message_json),
    #path('msgListner-json',views.listen_message_json)
    #path('get_contact_ajax/<str:id>', views.get_contact_ajax), 
    path('add_chat/<str:id>', views.add_chat), 
    
]
