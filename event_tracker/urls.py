from django.urls import path

from . import views

urlpatterns = [
    path('', views.EventTrackingView.as_view(), name='event_tracking'),
]
