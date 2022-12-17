"""eventsss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('user_handler/', include('user_handler.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from event_handler import views
from user_handler import views as user_views

urlpatterns = [
    path('', views.all_events, name="all_events"),
    #path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='user_handler/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user_handler/logout.html'), name='logout'),
    path('register/', user_views.register, name='register'),
    path('user_profile/', user_views.profile, name='user_profile'),
    path('create_event/', views.create_event, name='create_event'),
    path('all_events/<int:event_id>', views.current_event, name="cur_event"),
    #re_path(r'^event_list/page/(\d+)', views.all_events, name="all_events"),
    #
    path('creator_events/<int:event_id>/participants', views.view_participants, name='participants'),
    #
]
