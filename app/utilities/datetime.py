import calendar
import re
import time


class NeDateTime:
    @staticmethod
    def sleep(sec=1):
        """
        Sleep for given number of seconds
        :param sec: Seconds to sleep
        :return:
        """
        if sec is None or sec < 1:
            sec = 1
        print(f"Sleeping for {sec} seconds")
        time.sleep(sec)
        print(f"Awake again after sleeping for {sec} seconds")

    @staticmethod
    def nowIso():
        return app.utilities.datetime.now().isoformat()

    @staticmethod
    def yyyymmddhhmmss():
        return app.utilities.datetime.now().strftime("%Y%m%d%H%M%S")

    @staticmethod
    def now_in_seconds():
        # input datetime
        dt = app.utilities.datetime.now()
        return calendar.timegm(dt.timetuple())

    @staticmethod
    def yyyymmddhhmmss_int():
        return int(app.utilities.datetime.now().strftime("%Y%m%d%H%M%S"))

    @staticmethod
    def removeMilliseconds(datetimeval):
        if datetimeval is None or str(datetimeval).strip() == '':
            return datetimeval
        output = re.sub('(\..*)$', '', datetimeval)
        return output
