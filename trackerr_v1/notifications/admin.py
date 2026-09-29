from django.contrib import admin
from notifications.models import WhatsappNotification

@admin.register(WhatsappNotification)
class WhatsappNotificationAdmin(admin.ModelAdmin):
    # Show these fields in the list view
    list_display = ("id", "parcel_number", "sent_at","updated_at", "parcel_status", "message_status")

    # Add filters on the right-hand side
    list_filter = ("parcel_number", "parcel_status", "sent_at", "message_status")

    # Make fields searchable
    search_fields = ("parcel_number", "parcel_status", "sent_at", "message_status")

    # Control which fields show up in the form
    fields = ( "parcel_number","sent_at", "parcel_status")

    # Optional: make some fields read-only
    readonly_fields = ("sent_at",)
