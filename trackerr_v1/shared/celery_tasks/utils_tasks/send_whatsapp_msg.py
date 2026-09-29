#!/usr/bin/python3
from celery import shared_task
import os
from requests import post
from notifications.serializers import WhatsappNotificationSerializer

"""
   Send Whatsapp Tracking Notification
"""

def whatsapp_update(phone:str , country: str, **kwargs: dict) -> bool:

    url = "https://graph.facebook.com/v25.0/1305695025955311/messages"
    WHATSAPP_API_KEY = os.environ.get('WHATSAPP_API_KEY')
    headers = {
        "Content-Type" : "application/json",
        "Authorization": f"Bearer {WHATSAPP_API_KEY}"
            }
    
    country_code = "234" if country.lower() == "nigeria" else "233"

    status = kwargs.get('status')
    customer_name = kwargs.get('customer_name').title()
    vendor_name = kwargs.get('vendor').title()
    rider_name = kwargs.get('rider_name').title()
    rider_phone = kwargs.get('rider_phone').title()
    order_num = kwargs.get('parcel_number').upper()

    assigned_utility_name = "order_notification"
    in_transit_utility_name = "order_enroute"
    delivered_utility_name = "order_delivered"
    returned_utility_name = "order_returned"

    if rider_phone:
        if len(rider_phone) == 10:
            rider_phone = f"0{rider_phone}"

    if phone:
        if (len(phone) > 10):
            phone = phone[1:]

    data = {
      "messaging_product": "whatsapp",
      "to": f"{country_code}{phone}",
      "type": "template",
      "template": {
        "name": "3p_direct_integration_test_template",
        "language": { "code": "en" },
        "components": [
            {
                "type": "header",
                "parameters": [
                        {
                            "type": "image",
                            "image": {
                                "link": "https://pub-957e266fc78e498890ebfb00b91b52f6.r2.dev/whatsapp-messaging/Screenshot_11-9-2026_125321_trackerr-web101.vercel.app.jpeg"
                            }
                        }
                    ]
            },
          {"type": "body",
            "parameters": [
                {"type": "text", "parameter_name": "customer_name", "text" : customer_name},
                {"type": "text", "parameter_name": "order_number", "text" : order_num},
                {"type": "text", "parameter_name": "vendor_name", "text" : vendor_name},
                {"type": "text", "parameter_name": "rider_name", "text" : rider_name},
                {"type": "text", "parameter_name": "rider_phone", "text" : rider_phone},
            ]
        },
          ]
      }}


    if status in ["delivered", "returned", "in transit"]:
        button = {
              "type": "button",
              "sub_type": "url",
              "index": "0",
              "parameters": [
                  {
                      "type": "text",
                      "text": order_num
                  }
              ]
        }

        data['template']['components'].append(button)


    if status in ["delivered", "returned"]:
        param = [
            {"type": "text", "parameter_name": "customer_name", "text" : customer_name},
            {"type": "text", "parameter_name": "vendor_name", "text" : vendor_name},
        ]
        for item in data.get('template').get('components'):
            if item.get('type') == 'body':
                item['parameters'] = param

            elif item.get('type') == 'header':
                item['parameters'] = [{

                    "type": "text",
                    "parameter_name": "order_number",
                    "text": order_num
                    }]

    if status == 'assigned':
        data["template"]["name"] = assigned_utility_name
        req = post(url, headers=headers, json=data)


    elif status == 'in transit':
        data["template"]["name"] = in_transit_utility_name
        req = post(url, headers=headers, json=data)


    elif status == 'delivered':
        data["template"]["name"] = delivered_utility_name
        req = post(url, headers=headers, json=data)


    elif status == 'returned':
        data["template"]["name"] = returned_utility_name
        req = post(url, headers=headers, json=data)

    if req.status_code == 200:
        return True


@shared_task(bind=True, name='whatsapp_update')
def send_whatsapp_update(self, phone, country, **kwargs):
    is_sent = whatsapp_update(phone, country, **kwargs)
    country_code = '234' if country.lower() == 'nigeria' else '233'

    if (len(phone) > 10):
        phone = phone[1:11]
    if is_sent:
        data = {
            "receiver_phone": f"{country_code}{phone}",
            "parcel_number": kwargs['parcel_number'],
            "parcel_status": kwargs['status']
                }

        serializer = WhatsappNotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print('Whatsapp message sent to: ' + phone)
        else:
            print('Error Sending Whatsapp Msg: ',serializer.errors)

    else:
        print('Failed to send Whatsapp messeage sent with status {} to: {}'.format(kwargs['status'], phone))
