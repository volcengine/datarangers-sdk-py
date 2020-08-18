import constants
from event import Event
from header import Header
from user import User
import json, requests


class SendException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


def check_url(func):
    def wrapper(*args, **kw):
        if Collector.ssid_info_url and Collector.mp_url and Collector.app_url:
            return func(*args, **kw)
        else:
            raise SendException(constants.URL_ERROR)

    return wrapper


def modify_params(func):
    def wrapper(app_key: str, user: User, header: Header, events: list):
        for event in events:
            event.params = json.dumps(event.params)
        return func(app_key, user, header, events)

    return wrapper


class Collector:
    host = "snssdk.vpc.com"
    ssid_info_url = None
    app_url = None
    mp_url = None
    port = 31081
    ip = ""
    HTTP_PREFIX = "http://"
    APP_LOG_URL = "/service/2/app_log"
    SSID_INFO_URL = "/query/ssidinfo"
    MP_URL = "/v2/event/json"

    @staticmethod
    def set_host(host):
        Collector.host = host

    @staticmethod
    def set_port(port):
        Collector.port = port

    @staticmethod
    def set_ip(ip):
        Collector.ip = ip

    @staticmethod
    def set_app_url(app_url):
        Collector.app_url = app_url

    @staticmethod
    def set_mp_url(mp_url):
        Collector.mp_url = mp_url

    @staticmethod
    def set_ssid_info_url(ssid_url):
        Collector.ssid_info_url = ssid_url

    @staticmethod
    def set_ip_port(ip: str, port: int):
        Collector.set_ip(ip)
        Collector.set_port(port)
        Collector.set_app_url("{}{}:{}{}".format(Collector.HTTP_PREFIX, ip, port, Collector.APP_LOG_URL))
        Collector.set_mp_url("{}{}:{}{}".format(Collector.HTTP_PREFIX, ip, port, Collector.MP_URL))
        Collector.set_ssid_info_url("{}{}:{}{}".format(Collector.HTTP_PREFIX, ip, port, Collector.SSID_INFO_URL))

    @staticmethod
    def set_urls(url):
        Collector.set_app_url("{}{}{}".format(Collector.HTTP_PREFIX, url, Collector.APP_LOG_URL))
        Collector.set_mp_url("{}{}{}".format(Collector.HTTP_PREFIX, url, Collector.MP_URL))
        Collector.set_ssid_info_url("{}{}{}".format(Collector.HTTP_PREFIX, url, Collector.SSID_INFO_URL))

    @staticmethod
    def send_app_event(app_key: str, user: User, header: Header, event: Event):
        Collector.send_app_events(app_key, user, header, [event])

    @staticmethod
    def send_mp_event(app_key: str, user: User, header: Header, event: Event):
        Collector.send_mp_events(app_key, user, header, [event])

    @staticmethod
    @check_url
    @modify_params
    def send_mp_events(app_key: str, user: User, header: Header, events: list):
        Collector.get_ssid_did(user, header)
        user_ = {k: user.__dict__[k] for k in user.__dict__ if user.__dict__[k] is not None}
        msg = {
            "header": {k: header.__dict__[k] for k in header.__dict__ if header.__dict__[k] is not None},
            "events": [{k: event.__dict__[k] for k in event.__dict__ if event.__dict__[k] is not None} for event in
                       events],
            "user": user_
        }
        del msg["header"]["aid"]
        del msg["header"]["app_install_id"]
        msg["header"].update(user_)
        msg["header"]["app_key"] = app_key
        try:
            res = requests.post(Collector.mp_url, headers={"Host": Collector.host}, json=msg)
            result = json.loads(res.content)
            if "message" not in result or result["message"] != "success":
                raise SendException(constants.SEND_ERROR)
        except Exception as e:
            raise e

    @staticmethod
    @check_url
    def send_app_events(app_key: str, user: User, header: Header, events: list):
        Collector.get_ssid_did(user, header)
        user_ = {k: user.__dict__[k] for k in user.__dict__ if user.__dict__[k] is not None}
        msg = {
            "header": {k: header.__dict__[k] for k in header.__dict__ if header.__dict__[k] is not None},
            "event_v3": [{k: event.__dict__[k] for k in event.__dict__ if event.__dict__[k] is not None} for event in
                         events]
        }
        del msg["header"]["app_id"]
        msg["header"].update(user_)
        msg["header"]["app_key"] = app_key
        try:
            res = requests.post(Collector.app_url, headers={"Host": Collector.host}, json=msg)
            result = json.loads(res.content)
            if "message" not in result or result["message"] != "success":
                raise SendException(constants.SEND_ERROR)
        except Exception as e:
            raise e

    @staticmethod
    @check_url
    def get_ssid_did(user: User, header: Header):
        if header.app_id is None:
            raise SendException(constants.APP_ID_ERROR)
        if user.user_unique_id is None:
            raise SendException(constants.USER_UNIQUE_ID_ERROR)
        if user.ssid is None or user.device_id is None:
            msg = {
                "app_id": header.app_id,
                "user_unique_id": user.user_unique_id,
                "web_id": "1"
            }
            res = requests.post(Collector.ssid_info_url, json=msg)
            try:
                result = json.loads(res.content)
                if "ssid" in result and "device_id" in result:
                    user.set_ssid(result["ssid"])
                    user.set_device_id(result["device_id"])
                    user.set_web_id(result["device_id"])
                else:
                    raise SendException(constants.SSID_GET_ERROR)
            except Exception as e:
                raise e
