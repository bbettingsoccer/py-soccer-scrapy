from _datetime import datetime
import pytz
import tzlocal

from src.app.server.common.match_constants import MatchConstants


class TimezoneUtil:

    @staticmethod
    def convertTimezoneToLocalDateTime(dateTime_start: str, dateTime_end: str, timezone_from: str) -> dict:
        dateTimeObj = {}

        # CONVERT DATE/TIME FROM-String TO-DATE IN FORMAT
        dateStartObj_From = datetime.strptime(dateTime_start, MatchConstants.DATE_FORMAT_FULL)
        dateEndObj_From = datetime.strptime(dateTime_end, MatchConstants.DATE_FORMAT_FULL)

        # SET TIMEZONE BASED IN DATE FROM/ORIGIN
        timezone_From = pytz.timezone(timezone_from)
        dateStart_From = timezone_From.localize(dateStartObj_From)
        dateEnd_From = timezone_From.localize(dateEndObj_From)

        # SET TIMEZONE (SYSTEM-LOCAL) BASED IN DATE TO/DESTINATION
        timezone_current = tzlocal.get_localzone_name()
        timezone_To = pytz.timezone(timezone_current)

        # CONVERT DATE/TIME TO DATE/TIME LOCAL-SYSTEM/DATE
        dateStart_To = dateStart_From.astimezone(timezone_To)
        dateEnd_To = dateEnd_From.astimezone(timezone_To)

        dateStart_To = dateStart_To.strftime('%Y-%m-%d %H:%M:%S')
        dateEnd_To = dateEnd_To.strftime('%Y-%m-%d %H:%M:%S')

        dateTimeObj["datetimeStart"] = dateStart_To
        dateTimeObj["datetimeEnd"] = dateEnd_To

        print("datetimeStart", dateTimeObj["datetimeStart"])
        print("datetimeEnd", dateTimeObj["datetimeEnd"])

        return dateTimeObj

    @staticmethod
    def dateNowUTC() -> datetime:
        dt = datetime.now()
        formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_dt

    @staticmethod
    def getTimezones() -> dict:
        new_dict = {}
        timezone_country = {}
        for countrycode in pytz.country_timezones:
            timezones = pytz.country_timezones[countrycode]
            new_dict["countrycode"] = countrycode
            new_dict["timezones"] = timezones
            for timezone in timezones:
                timezone_country[timezone] = countrycode
        return new_dict
