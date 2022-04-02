"""
Copyright 2020 Beijing Volcano Engine Technology Co., Ltd.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
Apache License, Version 2.0
Home page of The Apache Software Foundation
"""
import json

from datarangers.collector.util import constants

from datarangers.collector.model.event import Event
from datarangers.collector.model.header import Header


class Message:
    def __init__(self):
        self.message = {"_format_name": constants.SDK_VERSION}
        self.header = Header()

    def set_user_unique_id(self, user_unique_id):
        self.header.set_user_unique_id(user_unique_id)
        self.message["user_unique_id"] = user_unique_id

    def set_device_id(self, device_id):
        self.message["device_id"] = device_id
        self.header.set_device_id(device_id)
        return self

    def set_client_ip(self, client_ip):
        self.message["client_ip"] = client_ip
        return self

    def set_trace_id(self, trace_id):
        self.message["trace_id"] = trace_id
        return self

    def set_app_type(self, app_type):
        self.message["app_type"] = app_type
        return self

    def set_app_id(self, app_id):
        self.message["app_id"] = app_id
        self.header.set_aid(app_id)
        return self

    def set_event(self, event_name: str, event_params: dict):
        if "event_v3" not in self.message:
            self.message["event_v3"] = []
        event = Event()
        event.set_event(event_name)
        event.set_params(event_params)
        self.message["event_v3"].append(event.get_events())
        return self

    def set_header(self, header: Header):
        self.header = header
        return self

    def merge(self):
        self.message["header"] = self.header.header

    def get_json(self):
        if "device_id" not in self.message:
            self.set_device_id(0)
        self.merge()
        return json.dumps(self.message)
