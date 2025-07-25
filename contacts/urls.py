from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_contacts, name='search'),
    path('create/', views.create_contact, name='create-contact'),
    path('contact/<int:pk>/delete/', views.delete_contact, name='delete_contact')
]
