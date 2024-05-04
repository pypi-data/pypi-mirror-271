from datetime import date, datetime, timedelta
from Kronos.costructors import TimeZones


class Converters:

    def __init__(self, dt=None, td=None):
        self.dt = dt
        self.td = td

    def date(self) -> date:
        """
        return the datetime.date version of the kronos
        Returns: datetime.date
        """
        return self.dt.date()

    def datetime(self) -> datetime:
        """
        return the datetime.datetime version of the kronos
        Returns: datetime
        """
        return self.dt

    def isoformat(self) -> str:
        """
        return the isoformat version of the kronos
        Returns: str
        """
        return self.dt.isoformat()

    def iso(self) -> str:
        """
        return the isoformat version of the kronos
        Returns: str
        """
        return self.isoformat()

    def timestamp(self) -> float:
        """
        return the timestamp version of the kronos
        Returns: float
        """
        return self.dt.timestamp()

    def ts(self) -> float:
        """
        return the timestamp version of the kronos
        Returns: float
        """
        return self.timestamp()

    def timedelta(self) -> timedelta:
        """
        return the timedelta version of kronos
        Returns: timedelta
        """
        return self.td

    def td(self) -> timedelta:
        """
        return the timedelta version of the kronos
        Returns: timedelta
        """
        return self.td

    def move_tz(self, tz):
        """modify the time accordingly to a new timezone"""
        if isinstance(tz, str): tz = TimeZones.dict_zones[tz]
        new_kronos = self.__class__()
        new_kronos.dt = self.dt.astimezone(tz=tz)
        return new_kronos

    def replace_tz(self, tz):
        """overwrite the timezone"""
        if isinstance(tz, str): tz = TimeZones.dict_zones[tz]
        new_kronos = self.__class__()
        new_kronos.dt = self.dt.replace(tzinfo=tz)
        return new_kronos

    def remove_tz(self):
        new_kronos = self.__class__()
        new_kronos.dt = self.dt.replace(tzinfo=None)
        return new_kronos
    #
    # @classmethod
    # def move_tz_from_list(cls, list_old_tz, tz):
    #     """overwrite the timezone from a list"""
    #     if isinstance(tz, str): tz = TimeZones.dict_zones[tz]
    #
    #     def move_tz_single(tz):
    #         return cls.move_tz(tz)
    #
    #     return list(map(move_tz_single, tz))
