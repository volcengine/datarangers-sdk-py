class User:
    def __init__(self, user_unique_id=None, device_id=None, web_id=None, ssid=None):
        self.user_unique_id = user_unique_id
        self.device_id = device_id
        self.web_id = web_id
        self.ssid = ssid

    def set_user_unique_id(self, user_unique_id):
        self.user_unique_id = user_unique_id
        return self

    def set_device_id(self, device_id):
        self.device_id = device_id
        return self

    def set_web_id(self, web_id):
        self.web_id = web_id
        return self

    def set_ssid(self, ssid):
        self.ssid = ssid
        return self

