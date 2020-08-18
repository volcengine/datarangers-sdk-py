import datetime


class Event:
    def __init__(self, event: str = None, local_time_ms: int = None, params: dict = None,
                 session_id: str = None, time: int = None):
        self.event = event
        self.local_time_ms = local_time_ms
        self.params = params
        self.session_id = session_id
        self.time = time
        if time:
            self.datetime = datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")

    def set_event(self, event):
        self.event = event
        return self

    def set_local_time_ms(self, local_time_ms):
        self.local_time_ms = local_time_ms
        return self

    def set_params(self, params):
        self.params = params
        return self

    def set_session_id(self, session_id):
        self.session_id = session_id
        return self

    def set_time(self, time):
        self.time = time
        self.datetime = datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")
        return self
