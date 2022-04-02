"""
Copyright 2020 Beijing Volcano Engine Technology Co., Ltd.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
Apache License, Version 2.0
Home page of The Apache Software Foundation
"""
import datetime
import time

from datarangers.collector.model.items import Items


class Event:
    def __init__(self):
        cur_time = int(time.time() * 1000)
        self.event = {
            "local_time_ms": cur_time,
            "datetime": datetime.datetime.fromtimestamp(cur_time / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            "params": {}
        }
        self.items = {}

    def set_event(self, event):
        self.event["event"] = event
        return self

    def set_local_time_ms(self, local_time_ms):
        self.event["local_time_ms"] = local_time_ms
        self.event["datetime"] = datetime.datetime.fromtimestamp(local_time_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
        return self

    def set_params(self, params):
        if isinstance(params, dict):
            for key in params:
                self.add_params(key, params.get(key))
        return self

    def add_params(self, key, value):
        if isinstance(value, Items):
            if value.get_item_name() not in self.items:
                self.items[value.get_item_name()] = []
            self.items[value.get_item_name()].append(value.get_item_id())
        elif ("rangers_items" or "_items") == key and isinstance(value, list):
            for item in value:
                if item["item_name"] not in self.items:
                    self.items[item["item_name"]] = []
                self.items[item["item_name"]].append(item["id"])
        else:
            self.event["params"][key] = value

    def set_session_id(self, session_id):
        self.event["session_id"] = session_id
        return self

    def set_event_id(self, event_id):
        self.event["event_id"] = event_id
        return self

    def set_ab_sdk_version(self, ab_sdk_version):
        self.event["ab_sdk_version"] = ab_sdk_version
        return self

    def get_events(self):
        if self.items:
            event_items = []
            for key in self.items:
                arr = []
                for item_id in self.items[key]:
                    arr.append({"id": item_id})

                event_items.append({
                    key: arr
                })
            self.add_params("__items", event_items)
        return self.event
