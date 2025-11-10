# agency/signals.py
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Booking

# store previous status before save
@receiver(pre_save, sender=Booking)
def booking_pre_save(sender, instance: Booking, **kwargs):
    if instance.pk:
        try:
            previous = Booking.objects.get(pk=instance.pk)
            instance._previous_status = previous.status
        except Booking.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance: Booking, created, **kwargs):
    """
    - On creation: send guest confirmation + admin notification.
    - On status change (confirmed/cancelled): send updated emails.
    """
    # prepare common context for templates
    ctx = {
        "booking": instance,
        "site_name": getattr(settings, "SITE_NAME", "Travel Agency"),
    }

    # determine admin recipients (use settings.ADMINS or fallback)
    admin_emails = [email for _, email in getattr(settings, "ADMINS", [])]
    if not admin_emails:
        admin_emails = [getattr(settings, "DEFAULT_FROM_EMAIL", "admin@example.com")]

    # --- On create: send booking confirmation to guest + admin notification ---
    if created:
        # Guest email (HTML + plain)
        subject_guest = f"[{ctx['site_name']}] Booking received — #{instance.id}"
        html_message = render_to_string("emails/booking_created_guest.html", ctx)
        plain_message = render_to_string("emails/booking_created_guest.txt", ctx)

        send_mail(
            subject_guest,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            html_message=html_message,
            fail_silently=False,
        )

        # Admin notification
        subject_admin = f"[{ctx['site_name']}] New booking #{instance.id}"
        html_admin = render_to_string("emails/booking_created_admin.html", ctx)
        plain_admin = render_to_string("emails/booking_created_admin.txt", ctx)
        send_mail(
            subject_admin,
            plain_admin,
            settings.DEFAULT_FROM_EMAIL,
            admin_emails,
            html_message=html_admin,
            fail_silently=True,
        )
        return

    # --- On status change: send status update when changed to confirmed or cancelled ---
    prev = getattr(instance, "_previous_status", None)
    new = instance.status
    if prev != new and new in ("confirmed", "cancelled"):
        # Guest status update
        subject_guest = f"[{ctx['site_name']}] Booking #{instance.id} — {new.title()}"
        html_message = render_to_string(f"emails/booking_{new}_guest.html", ctx)
        plain_message = render_to_string(f"emails/booking_{new}_guest.txt", ctx)
        send_mail(
            subject_guest,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            html_message=html_message,
            fail_silently=False,
        )

        # Admin notification about status change
        subject_admin = f"[{ctx['site_name']}] Booking #{instance.id} {new}"
        html_admin = render_to_string(f"emails/booking_{new}_admin.html", ctx)
        plain_admin = render_to_string(f"emails/booking_{new}_admin.txt", ctx)
        send_mail(
            subject_admin,
            plain_admin,
            settings.DEFAULT_FROM_EMAIL,
            admin_emails,
            html_message=html_admin,
            fail_silently=True,
        )
