from django.contrib import admin
from .models import Guesthouse, RoomType, Package, Transfer, Excursion, Booking

class RoomInline(admin.TabularInline):
    model = RoomType
    extra = 0

@admin.register(Guesthouse)
class GuesthouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_text', 'contact_info', 'rating')
    search_fields = ('name', 'location_text')
    inlines = [RoomInline]

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'guesthouse', 'capacity', 'price_per_night')
    list_filter = ('guesthouse',)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'base_price')

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('type', 'route', 'price')

@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'price')


# ✅ Custom admin actions for bookings
@admin.action(description="Mark selected bookings as Confirmed")
def mark_confirmed(modeladmin, request, queryset):
    count = queryset.update(status='confirmed')
    modeladmin.message_user(request, f"{count} booking(s) marked as confirmed.")

@admin.action(description="Mark selected bookings as Cancelled")
def mark_cancelled(modeladmin, request, queryset):
    count = queryset.update(status='cancelled')
    modeladmin.message_user(request, f"{count} booking(s) marked as cancelled.")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'guest_name', 'guesthouse', 'room_type',
        'check_in', 'check_out', 'status', 'total_price', 'created_at'
    )
    list_filter = ('status', 'guesthouse', 'created_at')
    search_fields = ('guest_name', 'email', 'phone')
    readonly_fields = ('created_at',)
    actions = [mark_confirmed, mark_cancelled]

    # ✅ Make status editable from the list view
    list_editable = ('status',)
