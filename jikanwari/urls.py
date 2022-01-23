from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('edit/<str:s>', views.edit, name='edit'),
    path('settings', views.settings, name='settings'),
    path('assignments', views.assignments, name='assignments'),
    path('edit_assignment/<int:pk>', views.edit_assignment, name='edit_assignment'),
    path('register_assignment', views.register_assignment, name='register_assignment'),
    path('register_assignments', views.register_assignments, name='register_assignments'),
    path('delete/<int:pk>', views.delete, name='delete'),
]