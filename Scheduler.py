import pycronofy
import datetime
import dateutil.parser
import pytz


class Scheduler:
    def __init__(self):
        self.cronofy = pycronofy.Client(access_token="wzOWhqxK-cmgld6AqZa6HA59qTNESn7o")
        self.calendars = {}
        self.events = []

        self.calendar_names_to_track = ["School", "Away"]
        self.calendars_to_track = []

        self.update()

    def update(self):
        calendar_list = self.cronofy.list_calendars()
        self.calendars = {}
        for calendar in calendar_list:
            self.calendars[calendar["calendar_id"]] = calendar
            if calendar["calendar_name"] in self.calendar_names_to_track:
                self.calendars_to_track.append(calendar)

        self.events = self.cronofy.read_events(
            calendar_ids=tuple([calendar.get("calendar_id") for calendar in self.calendars_to_track]),
            from_date=datetime.datetime.now(),
            to_date=datetime.datetime.now() + datetime.timedelta(days=5),
            tzid=pytz.timezone('EST')
        )

    def event_is_occurring(self):
        now = datetime.datetime.now()
        return self.event_will_be_occurring(now)

    def event_will_be_occurring(self, event_time):
        tz = pytz.timezone('EST')
        for event in self.events:
            print(event)
            start = dateutil.parser.parse(event["start"])
            start = start.replace(tzinfo=pytz.utc).astimezone(tz)
            start = start + datetime.timedelta(hours=1)  # off by 1 hour
            print("start: " + str(start))
            end = dateutil.parser.parse(event["end"])
            end = end.replace(tzinfo=pytz.utc).astimezone(tz)
            end = end + datetime.timedelta(hours=1)
            print("end: " + str(end))
            if start < event_time < end:
                return True
        return False
