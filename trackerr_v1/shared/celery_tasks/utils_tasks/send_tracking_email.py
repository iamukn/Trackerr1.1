from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task


@shared_task(bind=True, name="tracking_updates_email")
def send_tracking_updates_email(
    self,
    email,
    customer_name,
    parcel_number,
    status,
    vendor="",
    delivery_address="",
    eta="",
    items="",
    rider_name="",
    rider_phone="",
    is_subscribed=False,
):
    """
    Send Trackerr parcel tracking notification email.
    """

    if is_subscribed:
        return "Customer is subscribed; notification email skipped"

    customer_name = customer_name.split(" ")[0].capitalize()
    parcel_number = parcel_number.upper()

    # Handle tracking activation separately
    if isinstance(status, bool):

        if status is not True:
            return "Tracking activation email skipped"

        subject = "Yay! You can now track your delivery 🚚"
        template_status = "tracking_activated"

    else:
        status = status.lower().strip()

        status_config = {
            "pending": {
                "subject": f"Your parcel has been confirmed — Tracking #{parcel_number}",
            },
            "assigned": {
                "subject": "Your parcel is now with a rider 🚴",
            },
            "delivered": {
                "subject": "Your parcel has been delivered ✅",
            },
            "returned": {
                "subject": "Your parcel has been returned 🔄",
            },
            "cancelled": {
                "subject": "Your parcel delivery has been cancelled",
            },
            "canceled": {
                "subject": "Your parcel delivery has been cancelled",
            },
        }

        if status not in status_config:
            return f"Unsupported tracking status: {status}"

        subject = status_config[status]["subject"]

        # Normalize American/British spelling internally
        template_status = (
            "cancelled"
            if status in ["cancelled", "canceled"]
            else status
        )

    tracking_url = (
        f"https://trackerr.africa/track/{parcel_number}/"
    )

    context = {
        "subject": subject,
        "customer_name": customer_name,
        "parcel_number": parcel_number,
        "status": template_status,
        "vendor": vendor.title() if vendor else "",
        "delivery_address": delivery_address.title() if delivery_address else "",
        "eta": eta,
        "items": items.title() if items else "",
        "rider_name": rider_name.title() if rider_name else "",
        "rider_phone": rider_phone,
        "tracking_url": tracking_url,
    }

    # Render HTML email
    html_content = render_to_string(
        "emails/tracking_update.html",
        context,
    )

    # Plain-text equivalent
    if template_status == "pending":

        text_content = f"""
Hi {customer_name},

Your order has been successfully confirmed! 🎉

Here are your delivery details:

Tracking Number: {parcel_number}
Vendor: {context["vendor"]}
Delivery Address: {context["delivery_address"]}
Items: {context["items"]}
Expected Delivery Date: {eta}
Current Status: {template_status.capitalize()}

You can track your parcel in real time using the link below:

{tracking_url}

Thanks for choosing Trackerr.

Trackerr
Reliable deliveries. Real-time tracking. Peace of mind.
"""

    elif template_status == "assigned":

        text_content = f"""
Hi {customer_name},

Good news! Your parcel #{parcel_number} has been assigned to a rider and is now on its way for delivery.

Rider Name: {context["rider_name"]}
Rider Phone: {rider_phone}

You can track your parcel in real time once tracking has been activated by the rider.

Track your parcel:
{tracking_url}

Thanks for choosing Trackerr.

Trackerr
Reliable deliveries. Real-time tracking. Peace of mind.
"""

    elif template_status == "tracking_activated":

        text_content = f"""
Hi {customer_name},

Yay! Your parcel #{parcel_number} from {context["vendor"]} is now on its way.

You can now track your delivery in real time as the rider makes their way to you.

Tracking Link:
{tracking_url}

Thanks for choosing Trackerr.

Trackerr
Reliable deliveries. Real-time tracking. Peace of mind.
"""

    elif template_status == "delivered":

        text_content = f"""
Hi {customer_name},

Your parcel #{parcel_number} has been successfully delivered. We hope you had a great experience.

If you did not receive your parcel, please contact {context["vendor"]} as soon as possible.

Thank you for choosing Trackerr.

Trackerr
Reliable deliveries. Real-time tracking. Peace of mind.
"""

    elif template_status == "returned":

        text_content = f"""
Hi {customer_name},

We're sorry! Your parcel #{parcel_number} from {context["vendor"]} has been returned to the vendor.

You may contact your vendor for further details or arrange a redelivery.

Thanks for choosing Trackerr.

Trackerr
Reliable deliveries. Real-time tracking. Peace of mind.
"""

    elif template_status == "cancelled":

        text_content = f"""
Hi {customer_name},

The delivery for your parcel #{parcel_number} from {context["vendor"]} has been cancelled.

Please contact the vendor for more information.

We apologize for the inconvenience.

Trackerr
Reliable deliveries. Real-time tracking. Peace of mind.
"""

    else:
        text_content = f"""
Hi {customer_name},

There is an update regarding your parcel #{parcel_number}.

Current Status: {template_status.capitalize()}

Track your parcel:
{tracking_url}

Thanks for choosing Trackerr.

Trackerr
Reliable deliveries. Real-time tracking. Peace of mind.
"""

    try:

        email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        email_message.attach_alternative(
            html_content,
            "text/html",
        )

        email_message.send(fail_silently=False)

        if isinstance(status, bool):
            return "tracking activated status notification email sent"

        return f"{template_status.title()} status notification email sent"

    except Exception as e:
        raise e
