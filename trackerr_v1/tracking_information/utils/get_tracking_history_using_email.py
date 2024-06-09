#!/usr/bin/env python3
from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer

""" Returns tracking numbers linked to a parcular customer """

def retrieve_history(email: str) -> list:
    if not email or '@' not in email:
        return {'detail': 'Enter a valid email address!'}
    
    try:
        tracking_info = Tracking_info.objects.filter(customer_email=email)
        serializer = Tracking_infoSerializer(tracking_info, many=True)
        datas =serializer.data
        for data in datas:
            if data.get('status') == 'Pending':
                info = {'details': {
                    'status1': f"{data.get('parcel_number')} is {data.get('status').lower()}",
                    'status2': f"Estimated time of arrival~ {data.get('status').lower()}"}}
                data.update(info)
            elif data.get('status') == 'in transit':
                info = {'details': {
                    'status1': f"{data.get('parcel_number')} is on the way",
                    'status2': f"Estimated time of arrival~today"
                        }
                    }
                data.update(info)
            elif data.get('status') == 'returned':
                info = {'details': {
                    'status1': f"{data.get('parcel_number')} has been returned",
                    'status2': f"Estimated time of arrival~{data.get('status').lower()}"
                    }
                        }
                data.update(info)
            elif data.get('status') == 'delivered':
                info = {'details': {
                    'status1': f"{data.get('parcel_number')} has been delivered",
                    'status2': "Arrived",
                    }    }
                data.update(info)

            else:
                info = {'details': {
                    'status1': f"{data.get('parcel_number')} has been canceled",
                    'status2': "",
                    }    
                        }
                data.update(info)
        return datas
    except Exception as e:
        return e
