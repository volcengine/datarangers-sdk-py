# encoding: utf-8
from datarangers.collector.event_collector import EventCollector
import os

EventCollector.init(
    {
        "headers": {
            "Host": os.getenv("HOST")
        },
        "http_timeout": 0.2,
        "domain": os.getenv("DOMAIN"),
        "save": False,
        "log_max_bytes": 100 * 1024,
        "log_file_name": "datarangers",
        "log_file_path": "logs/datarangers/",
        "queue_length": 204800,
        "thread_count": 4
    }
)

app_id = os.getenv("APP_ID")


def send_app():
    device_id = 7542966151014286350
    EventCollector.send_app_event('uuid', app_id, {}, 'app_event_ab_sdk', {}, ab_sdk_version="11")
    EventCollector.send_app_event('', app_id, {}, 'app_event_test1', {}, device_uniq_id=device_id)
    EventCollector.send_app_event('', app_id, {}, 'app_event_test2', {}, device_uniq_id=device_id,
                                  ab_sdk_version="1")
    EventCollector.send_app_event('', app_id, {}, ['app_event_test3', 'app_event_test4'], [{}, {}],
                                  device_uniq_id=device_id)
    EventCollector.send_app_event('', app_id, {}, ['app_event_test5', 'app_event_test6'], [{}, {}],
                                  device_uniq_id=device_id,
                                  ab_sdk_version=["1", "2"])


def send_web():
    web_id = 2
    EventCollector.send_web_event('', app_id, {}, 'web_event_test1', {}, device_uniq_id=web_id)
    EventCollector.send_web_event('', app_id, {}, 'web_event_test2', {}, device_uniq_id=web_id,
                                  ab_sdk_version="1")
    EventCollector.send_web_event('', app_id, {}, ['web_event_test3', 'web_event_test4'], [{}, {}],
                                  device_uniq_id=web_id)
    EventCollector.send_web_event('', app_id, {}, ['web_event_test5', 'web_event_test6'], [{}, {}],
                                  device_uniq_id=web_id,
                                  ab_sdk_version=["1", "2"])


def send_mp():
    web_id = 3
    EventCollector.send_mp_event('', app_id, {}, 'mp_event_test1', {}, device_uniq_id=web_id)
    EventCollector.send_mp_event('', app_id, {}, 'mp_event_test2', {}, device_uniq_id=web_id, ab_sdk_version="1")
    EventCollector.send_mp_event('', app_id, {}, ['mp_event_test3', 'mp_event_test4'], [{}, {}],
                                 device_uniq_id=web_id)
    EventCollector.send_mp_event('', app_id, {}, ['mp_event_test5', 'mp_event_test6'], [{}, {}],
                                 device_uniq_id=web_id,
                                 ab_sdk_version=["1", "2"])


if __name__ == '__main__':
    send_app()
    # send_web()
    # send_mp()
