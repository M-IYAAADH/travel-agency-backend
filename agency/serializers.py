from rest_framework import serializers
from .models import Guesthouse, RoomType, Package, Transfer, Excursion, Booking

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'

class GuesthouseSerializer(serializers.ModelSerializer):
    rooms = RoomTypeSerializer(many=True, read_only=True)
    class Meta:
        model = Guesthouse
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

class ExcursionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('status', 'created_at')
