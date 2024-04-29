#!/usr/bin/python
from datetime import datetime, timedelta
from user.models import User
from typing import Dict, List
from tracking_information.models import Tracking_info


""" Fetches the counts for tracking generated in the last 7 days """


class ActivityChart(object):
    """  Fetches the counts for tracking generated in the last 7 days and month """
    today = datetime.today()
    def _get_query_set(self, user_id: int) -> List: 
        # fetches the data from the database
        try:
            self.query_set = Tracking_info.objects.filter(owner=user_id)
            return self.query_set
        except Exception as e:
            return e

    def last_seven_days(self, user: User) -> Dict:
        """ fetches the count of tracking generated today
        Arg:
            user -> The user object
        Return:
            Dictionary
        """
        last_seven = {}

        query_set = self._get_query_set(user)
        today = self.today
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

    def last_month_count(self, user: User) -> List:
        """ gets the tracking number count generated by a business owner
        Arg:
            user -> The User object
        Return:
            A dictionary of weeks with counts of tracking generated that week
        """
        query_set = self._get_query_set(user.id)
        
        week1 = query_set.filter(date_of_purchase__range=(self.today - timedelta(days=28), self.today - timedelta(days=23))).count()
        week2 = query_set.filter(date_of_purchase__range=(self.today - timedelta(days=22), self.today - timedelta(days=16))).count()
        week3 = query_set.filter(date_of_purchase__range=(self.today - timedelta(days=15), self.today - timedelta(days=9))).count()        
        week4 = query_set.filter(date_of_purchase__range=(self.today - timedelta(days=8), self.today)).count()
        weekly_count = {'Week One': week1, 'Week Two': week2, 'Week Three': week3, 'Week Four': week4}
        return weekly_count
