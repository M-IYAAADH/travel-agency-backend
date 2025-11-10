from django.urls import path
from . import views

urlpatterns = [
    path('guesthouses/', views.GuesthouseListAPIView.as_view(), name='guesthouse-list'),
    path('guesthouses/<int:pk>/', views.GuesthouseDetailAPIView.as_view(), name='guesthouse-detail'),

    path('packages/', views.PackageListAPIView.as_view(), name='package-list'),
    path('transfers/', views.TransferListAPIView.as_view(), name='transfer-list'),
    path('excursions/', views.ExcursionListAPIView.as_view(), name='excursion-list'),

    path('bookings/', views.BookingCreateAPIView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', views.BookingRetrieveAPIView.as_view(), name='booking-detail'),
]
