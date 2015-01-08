from datetime import datetime

class Schedule(object):
    WEEK_ONE = datetime(2014, 9, 2, 9)

    def week(self):
        time_difference = datetime.now() - self.WEEK_ONE
        return (time_difference.days/7)+1

    def season_year(self):
        return 2014
