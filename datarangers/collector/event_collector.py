"""
Copyright 2020 Beijing Volcano Engine Technology Co., Ltd.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
Apache License, Version 2.0
Home page of The Apache Software Foundation
"""
import queue
import logging
from datarangers.collector.config.collector_config import dataRangersSdkConfig, DataRangersSdkConfig
from datarangers.collector.model.event import Event
from datarangers.collector.model.header import Header
from datarangers.collector.model.items_method import ItemsMethod
from datarangers.collector.model.message import Message
from datarangers.collector.model.profile_method import ProfileMethod


class EventCollector:
    __init_status = False

    @staticmethod
    def send_app_event(user_unique_id: str, app_id: int, custom: dict, event_name, event_params,
                       device_type=None, device_uniq_id=None, ab_sdk_version=None, local_time_ms=None):
        r""" send app event

        :param user_unique_id: uuid
        :param app_id: app id
        :param custom
        :param event_name,event_params,ab_sdk_version,local_time_ms
            if isinstance(event_name, str):
                isinstance(event_params,dict) -> event_params should be a dict
            else if isinstance(event_name, list):
                isinstance(event_params,list) and len(event_params) == len(event_name)
                which mean event_name[n]'s params is event_params[n],
                ab_sdk_version[n]'s params is ab_sdk_version[n],
                local_time_ms[n]'s params is local_time_ms[n]

        :param device_type: ["android","ios"]
        :param device_uniq_id: device identification
        :param ab_sdk_version: ab_sdk_version
        :param local_time_ms: event time of millisecond
        """
        EventCollector.__collector("app", user_unique_id, app_id, custom, event_name, event_params, device_type,
                                   device_uniq_id, ab_sdk_version, local_time_ms)

    @staticmethod
    def send_mp_event(user_unique_id: str, app_id: int, custom: dict, event_name, event_params,
                      device_uniq_id=None, ab_sdk_version=None, local_time_ms=None):
        r""" send mp event

        :param user_unique_id: uuid
        :param app_id: app id
        :param custom
        :param event_name,event_params,ab_sdk_version,local_time_ms
            if isinstance(event_name, str):
                isinstance(event_params,dict) -> event_params should be a dict
            else if isinstance(event_name, list):
                isinstance(event_params,list) and len(event_params) == len(event_name)
                which mean event_name[n]'s params is event_params[n],
                ab_sdk_version[n]'s params is ab_sdk_version[n],
                local_time_ms[n]'s params is local_time_ms[n]

        :param device_uniq_id: device identification
        :param ab_sdk_version: ab_sdk_version
        :param local_time_ms: event time of millisecond
        """
        EventCollector.__collector("mp", user_unique_id, app_id, custom, event_name, event_params,
                                   device_uniq_id=device_uniq_id, ab_sdk_version=ab_sdk_version,
                                   local_time_ms=local_time_ms)

    @staticmethod
    def send_web_event(user_unique_id: str, app_id: int, custom: dict, event_name, event_params,
                      device_uniq_id=None, ab_sdk_version=None, local_time_ms=None):
        r""" send web event

        :param user_unique_id: uuid
        :param app_id: app id
        :param custom
        :param event_name,event_params, ab_sdk_version,local_time_ms
            if isinstance(event_name, str):
                isinstance(event_params,dict) -> event_params should be a dict
            else if isinstance(event_name, list):
                isinstance(event_params,list) and len(event_params) == len(event_name)
                which mean event_name[n]'s params is event_params[n],
                ab_sdk_version[n]'s params is ab_sdk_version[n]
                local_time_ms[n]'s params is local_time_ms[n]

        :param device_uniq_id: device identification
        :param ab_sdk_version: ab_sdk_version
        :param local_time_ms: event time of millisecond
        """
        EventCollector.__collector("web", user_unique_id, app_id, custom, event_name, event_params,
                                   device_uniq_id=device_uniq_id, ab_sdk_version=ab_sdk_version,
                                   local_time_ms=local_time_ms)

    @staticmethod
    def send_event(app_type: str, user_unique_id: str, app_id: int, header: Header, event: Event, device_uniq_id=None):
        """
        :param app_type: app type, only: app,web,mp
        :param user_unique_id: uuid
        :param app_id: app_id
        :param header: header
        :param event: event
        :param device_uniq_id: device_id
        """
        if not EventCollector.__init_status:
            raise RuntimeError("please init sdk config before use it")
        if (not header) or (not event):
            raise RuntimeError("header or event cannot be None")
        message = Message()
        message.set_header(header)
        message.set_app_type(app_type)
        message.set_app_id(app_id)
        message.set_user_unique_id(user_unique_id)
        message.add_event(event)
        if device_uniq_id:
            message.set_device_id(device_uniq_id)

        EventCollector.__send_event(message)


    @staticmethod
    def profile_set(user_unique_id: str, app_id: int, event_params):
        r""" send app event

        :param user_unique_id: uuid
        :param app_id: app id
        :param event_params: dict, set user profile
        """
        EventCollector.__collector("app", user_unique_id, app_id, None, ProfileMethod.SET.value, event_params)

    @staticmethod
    def profile_unset(user_unique_id: str, app_id: int, event_params: list):
        r""" send app event

        :param user_unique_id: uuid
        :param app_id: app id
        :param event_params: list, unset user profile
        """
        params = {}
        for p in event_params:
            params[p] = "python"
        EventCollector.__collector("app", user_unique_id, app_id, None, ProfileMethod.UNSET.value, event_params)

    @staticmethod
    def profile_set_once(user_unique_id: str, app_id: int, event_params):
        r""" send app event

        :param user_unique_id: uuid
        :param app_id: app id
        :param event_params: dict, set only once user profile
        """
        EventCollector.__collector("app", user_unique_id, app_id, None, ProfileMethod.SET_ONCE.value, event_params)

    @staticmethod
    def profile_increment(user_unique_id: str, app_id: int, event_params):
        r""" send app event

        :param user_unique_id: uuid
        :param app_id: app id
        :param event_params: dict
            params's value should be integer
        """
        EventCollector.__collector("app", user_unique_id, app_id, None, ProfileMethod.INCREMENT.value, event_params)

    @staticmethod
    def profile_append(user_unique_id: str, app_id: int, event_params):
        r""" send app event

        :param user_unique_id: uuid
        :param app_id: app id
        :param event_params: dict
            params's value should be list of string
        """
        EventCollector.__collector("app", user_unique_id, app_id, None, ProfileMethod.APPEND.value, event_params)

    @staticmethod
    def item_set(app_id: int, item_name, items_params: list):
        r"""send item set event

        :param app_id: app id
        :param item_name: item_name
        :param items_params:list of dict
            list of items: item should be a dict, item_name and item_value are necessary
        """
        for item_params in items_params:
            item_params["item_name"] = item_name
            if "item_id" not in item_params:
                item_params["item_id"] = item_params["id"]
            del item_params["id"]
        set_events = [ItemsMethod.SET.value for _ in range(len(items_params))]
        EventCollector.__collector("app", "__rangers", app_id, None, set_events, items_params)

    @staticmethod
    def item_unset(app_id: int, id, item_name, item_params: list):
        r""" unset item

        :param app_id: app id
        :param item_name: item_name
        :param item_params:list
        """
        params = {"item_id": id, "item_name": item_name}
        for p in item_params:
            params[p] = "python"
        EventCollector.__collector("app", "__rangers", app_id, None, ItemsMethod.UNSET.value, params)

    @staticmethod
    def __collector(app_type: str, user_unique_id: str, app_id: int, custom: dict, event_name, event_params,
                    device_type=None, device_uniq_id=None, ab_sdk_version=None, local_time_ms=None):
        if not EventCollector.__init_status:
            raise RuntimeError("please init sdk config before use it")
        message = Message()
        message.set_app_type(app_type)
        message.set_app_id(app_id)
        message.set_user_unique_id(user_unique_id)
        if custom:
            message.header.set_custom(custom)
        if device_type and device_uniq_id:
            device_type = str(device_type).upper()
            if device_type == "IOS":
                message.header.set_os("ios")
                message.header.set_vendor_id(device_uniq_id)
            elif device_type == "ANDROID":
                message.header.set_os("android")
                message.header.set_openudid(device_uniq_id)
        elif device_uniq_id:
            message.set_device_id(device_uniq_id)
        if not event_params:
            if isinstance(event_name, str):
                event_params = {}
            elif isinstance(event_name, list):
                event_params = {[] for i in range(len(list))}
        if isinstance(event_name, str) and isinstance(event_params, dict):
            message.set_event(event_name=event_name, event_params=event_params,
                              ab_sdk_version=ab_sdk_version, local_time_ms=local_time_ms)
        elif isinstance(event_name, list) and isinstance(event_params, list):
            for i in range(min(len(event_name), len(event_params))):
                name = event_name[i]
                if isinstance(name, ProfileMethod):
                    event_name_current = name.value
                else:
                    event_name_current = str(event_name[i]).lower()
                ab_sdk_version_current = None
                if isinstance(ab_sdk_version, list):
                    ab_sdk_version_current = ab_sdk_version[i]
                local_time_ms_current = None
                if isinstance(local_time_ms, list):
                    local_time_ms_current = local_time_ms[i]
                message.set_event(event_name_current, event_params[i], ab_sdk_version_current, local_time_ms_current)
        else:
            logging.error("event_name or event_params are invalid! event_name:{};event_params:{}".format(event_name,
                                                                                                         event_params))
        EventCollector.__send_event(message)

    @staticmethod
    def __send_event(message):
        if dataRangersSdkConfig.is_save():
            dataRangersSdkConfig.sdk_logger.debug(message.get_json())
        elif dataRangersSdkConfig.is_sync():
            session = DataRangersSdkConfig.init_session()
            # 内部捕获了异常
            DataRangersSdkConfig.http_send(message, session)
            session.close()
        else:
            try:
                dataRangersSdkConfig.sdk_queue.put(message, block=True, timeout=0.01)
            except queue.Full as e:
                logging.error("Queue fulled!")
                logging.exception(e)
                dataRangersSdkConfig.sdk_error_logger.debug(message.get_json())

    @staticmethod
    def init(conf: dict):
        dataRangersSdkConfig.init(conf)
        EventCollector.__init_status = True

