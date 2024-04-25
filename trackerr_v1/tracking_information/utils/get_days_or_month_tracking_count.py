#!/usr/bin/python
from datetime import datetime, timedelta
from typing import Dict, List
from tracking_information.models import Tracking_info


""" Fetches the counts for tracking generated in the last 7 days """


class ActivityChart(object):
    """  Fetches the counts for tracking generated in the last 7 days and month """
    def _get_query_set(self, user_id: int) -> List: 
        # fetches the data from the database
        self.query_set = Tracking_info.objects.filter(owner=user_id)
        return self.query_set

    def last_seven_days(self, user: int) -> Dict:
        """ fetches the count of tracking generated today
        Arg:
            user -> The user object
        Return:
            Dictionary
        """
        last_seven = {}

        query_set = self._get_query_set(user)
        today = datetime.today()
        count = query_set.filter(date_of_purchase=today).count()
        last_seven[today.strftime("%a")] = count

        # fetches the count of tracking generated last 6 days
        for day in range(1, 7, 1):
            day_date = timedelta(days=day)
            date = today - day_date
            count = query_set.filter(date_of_purchase=date).count()
            last_seven[date.strftime("%a")] = count
        last_seven["Thur"] = last_seven["Thu"]
        custom_order = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
        sorted_last_seven = {day: last_seven[day] for day in custom_order}

        return sorted_last_seven
