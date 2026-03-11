from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),

    # Listings
    path('listings/', views.listing_list, name='listing_list'),
    path('listings/create/', views.listing_create, name='listing_create'),
    path('listings/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listings/<int:pk>/edit/', views.listing_edit, name='listing_edit'),
    path('listings/<int:pk>/delete/', views.listing_delete, name='listing_delete'),
    path('listings/mine/', views.my_listings, name='my_listings'),

    # Requests
    path('listings/<int:listing_pk>/request/', views.request_create, name='request_create'),
    path('requests/', views.my_requests, name='my_requests'),
    path('requests/<int:pk>/status/', views.request_update_status, name='request_update_status'),
    path('requests/<int:pk>/withdraw/', views.request_withdraw, name='request_withdraw'),

    # Profile
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<int:pk>/', views.profile_view, name='profile_view_other'),
]
