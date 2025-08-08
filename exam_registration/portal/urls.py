from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.exam_session_list, name='exam_session_list'),
    path('register/<int:session_id>/', views.register_for_session, name='register_for_session'),
    path('my_registrations/', views.my_registrations, name='my_registrations'),
]
