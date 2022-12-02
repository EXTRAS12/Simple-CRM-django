from django.urls import path

from . import views


urlpatterns = [
    path('', views.clients_list, name='clients_list'),
    path('<int:pk>', views.clients_detail, name='clients_detail'),
    path('add-client/', views.add_client, name='add_client'),
    path('<int:pk>/delete/', views.clients_delete, name='clients_delete'),
    path('<int:pk>/edit/', views.clients_edit, name='clients_edit'),
]