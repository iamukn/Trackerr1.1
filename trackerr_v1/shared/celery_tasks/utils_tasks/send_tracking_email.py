#!/usr/bin/python3
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

"""
   Send Tracking Updates Notification email
"""

@shared_task(bind=True, name='tracking_updates_email')
def send_tracking_updates_email(self, email, customer_name, parcel_number,
                                status, vendor="", delivery_address="", eta="", items="", rider_name="", 
                                rider_phone="", is_subscribed=False
                                ):

    if not is_subscribed:
        # handles updates emails based on status
        customer_name = customer_name.split(' ')[0]

        if status.lower() == 'pending':
            subject = f'Your parcel has been confirmed — Tracking #{parcel_number}'

            message = """
                    Hi {},

                    Your order has been successfully confirmed! 🎉

                    Here are your delivery details:
                    - Tracking Number: {}
                    - Vendor: {}
                    - Delivery Address: {}
                    - Items: {} etc...
                    - Expected Delivery Date: {}
                    - Current Status: {}

                    You can track your parcel in real time using the link below:
                    https://thisiswherethetrackinglinkwillgo.com/{}/

            """.format(customer_name.capitalize(), parcel_number.upper(), 
                        vendor.title(), delivery_address.title(), items.title(), eta,
                        status.capitalize(), parcel_number
                        )


        elif status.lower() == 'assigned':
            subject = 'Your parcel is now with a rider 🚴'
            message = """
                Hi {},

                Good news! Your parcel #{} has been assigned to a rider and is now on its way for delivery.

                - Rider Name: {}
                - Rider Phone: {}

                You can track your parcel in real time here:
                Link: https://trackparcelhere.com/{}/

                We’ll notify you once it’s delivered.

                Trackerr
                Reliable deliveries. Real-time tracking. Peace of mind.

            """.format(customer_name.capitalize(),parcel_number.upper(), rider_name.title(), rider_phone, parcel_number.upper(),)

        elif status.lower() == 'delivered':
            subject = 'Your parcel has been delivered ✅'
            message = """
                Hi {},

                Your parcel #{} has been successfully delivered. We hope you had a great experience.
                If you didn’t receive it, please contact the shipper '{}' as soon as possible!

                Thank you for choosing Trackerr!

                Trackerr,
                Reliable deliveries. Real-time tracking. Peace of mind.

            """.format(customer_name.capitalize(), parcel_number.upper(), vendor.title())

        elif status.lower() == 'returned':
            subject = 'Your parcel has been returned 🔄'
            message = """
                Hi {},

                We’re sorry! Your parcel Tracking #{} from {} has been returned to the vendor.
                You may contact your vendor for further details or arrange a redelivery.

                Trackerr,
                Reliable deliveries. Real-time tracking. Peace of mind.
            """.format(customer_name.capitalize(), parcel_number.upper(), vendor.title() )

        elif status.lower() in ['cancelled', 'canceled']:
            subject = 'Your parcel delivery has been canceled'
            message = """
                Hi {},

                The delivery for your parcel #{} from {} has been canceled.
                Kindly contact the vendor for more information.

                We apologize for the inconvenience.
                
                Trackerr
                Reliable deliveries. Real-time tracking. Peace of mind.

            """.format(customer_name.capitalize(), parcel_number.upper(), vendor.title())

        from_email = settings.EMAIL_HOST_USER
        recipient_email = [email,]

        try:
            from_header = "Order Confirmation" if status == 'pending' else "Trackerr Delivery"
            send_mail(
                subject=subject,
                message=message,
                from_email=from_header,
                recipient_list=recipient_email,
                fail_silently = False,
                    )
            return f"{status.title()} status notification email sent"
        except Exception as e:
            raise e
            return f"unable to send {status} updates email"
