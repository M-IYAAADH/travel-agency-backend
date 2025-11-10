from rest_framework import generics
from .models import Guesthouse, Package, Transfer, Excursion, Booking
from .serializers import GuesthouseSerializer, PackageSerializer, TransferSerializer, ExcursionSerializer, BookingSerializer

# Guesthouse list & detail
class GuesthouseListAPIView(generics.ListAPIView):
    queryset = Guesthouse.objects.all()
    serializer_class = GuesthouseSerializer

class GuesthouseDetailAPIView(generics.RetrieveAPIView):
    queryset = Guesthouse.objects.all()
    serializer_class = GuesthouseSerializer

# Packages, transfers, excursions
class PackageListAPIView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class TransferListAPIView(generics.ListAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

class ExcursionListAPIView(generics.ListAPIView):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer

# Create booking
class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
