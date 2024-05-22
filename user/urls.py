from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profilechange/', views.profilechange, name='profilechange'),
    path('profile/', login_required(views.profile), name='profile'),
    path('rooms/', views.chat_rooms, name='chat_rooms'),
    path('rooms/<int:room_id>/', views.chat_room, name='chat_room'),
    path('create/', login_required(views.create_chat_room), name='create_chat_room'),
    path('delete/<int:chat_room_id>/', views.delete_chat_room, name='delete_chat_room'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)