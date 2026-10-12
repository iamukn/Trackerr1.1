from tracking_information.models import Tracking_info


def compute_referral_data(businesses, data, user):
    referrals_record = []
    total_trackings = 0
    coins_per_tracking = 10

    for business in businesses:
        all_trackings = Tracking_info.objects.filter(owner=business.id)
        tracking_count = len(all_trackings)
        total_trackings += tracking_count - 5 if tracking_count > 5 else 0

        business_data = {
                'business_name': str(business.business_owner.business_name).lower(),
                'tracking_numbers': tracking_count,
                'total_earned': tracking_count * coins_per_tracking,
                'country': str(business.country),
                'date_joined': business.date_joined.strftime('%d-%m-%Y'),
                'status': 'active' if business.is_active else 'inactive'
                }

        # add to existing data
        referrals_record.append(business_data)
    data['total_tracking_numbers'] = total_trackings
    data['referrals'] = referrals_record
    total_coins_earned = total_trackings * coins_per_tracking
    data['total_coins_earned'] = total_coins_earned
    data['available_coins'] = total_coins_earned - user.total_coins_withdrawn
    return data
