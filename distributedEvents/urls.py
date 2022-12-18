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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('user_handler/', include('user_handler.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from event_handler import views
from user_handler import views as user_views
from creator_handler import views as creator_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_event/', views.create_event, name='create_event'),
    path('all_events/<int:event_id>', views.cur_event, name="cur_event"),
    path('', views.all_events, name="all_events"),
    re_path(r'^event_list/page/(\d+)', views.all_events, name="all_events"),

    path('register/', user_views.register, name='register'),
    path('user_profile/', user_views.profile, name='user_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='user_handler/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user_handler/logout.html'), name='logout'),

    path('events/edit/<int:event_id>/venues/', creator_views.venues_list, name="test"),
    path('events/edit/<int:event_id>/venues/create', creator_views.create_venue, name="create_venue"),
    path('events/edit/<int:event_id>/venues/delete', creator_views.delete_venue, name="delete_venue"),

    # path('events/edit/<int:event_id>/venues/edit/<int:venue_id>', creator_views., name=""),
    # path('events/edit/<int:event_id>', creator_views., name=""),
    # path('events/edit/<int:event_id>', creator_views., name=""),
    # path('events/edit/<int:event_id>', creator_views., name=""),
]
