"""
Copyright 2020 Beijing Volcano Engine Technology Co., Ltd.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
Apache License, Version 2.0
Home page of The Apache Software Foundation
"""
import time


class Header:
    def __init__(self):
        tz_offset = time.localtime().tm_gmtoff
        self.header = {
            "tz_offset": tz_offset,
            "timezone": int(tz_offset / 60 / 60),
            "device_id": 1
        }

    def set_vendor_id(self, vendor_id):
        self.header["vendor_id"] = vendor_id
        return self

    def add_custom(self, key, value):
        if "custom" not in self.header:
            self.header["custom"] = {}
        self.header["custom"][key] = value

    def set_custom(self, custom: dict):
        if "custom" not in self.header:
            self.header["custom"] = {}
        if custom:
            self.header["custom"].update(custom)
        return self

    def set_aid(self, aid):
        self.header["aid"] = aid
        return self

    def set_app_language(self, app_language):
        self.header["app_language"] = app_language
        return self

    def set_app_name(self, app_name):
        self.header["app_name"] = app_name
        return self

    def set_app_region(self, app_region):
        self.header["app_region"] = app_region
        return self

    def set_app_version(self, app_version):
        self.header["app_version"] = app_version
        return self

    def set_app_version_minor(self, app_version_minor):
        self.header["app_version_minor"] = app_version_minor
        return self

    def set_build_serial(self, build_serial):
        self.header["build_serial"] = build_serial
        return self

    def set_carrier(self, carrier):
        self.header["carrier"] = carrier
        return self

    def set_channel(self, channel):
        self.header["channel"] = channel
        return self

    def set_client_ip(self, client_ip):
        self.header["client_ip"] = client_ip
        return self

    def set_clientudid(self, clientudid):
        self.header["clientudid"] = clientudid
        return self

    def set_cpu_abi(self, cpu_abi):
        self.header["cpu_abi"] = cpu_abi
        return self

    def set_device_id(self, device_id):
        self.header["device_id"] = device_id
        return self

    def set_device_brand(self, device_brand):
        self.header["device_brand"] = device_brand
        return self

    def set_device_manufacturer(self, device_manufacturer):
        self.header["device_manufacturer"] = device_manufacturer
        return self

    def set_device_model(self, device_model):
        self.header["device_model"] = device_model
        return self

    def set_device_type(self, device_type):
        self.header["device_type"] = device_type
        return self

    def set_display_name(self, display_name):
        self.header["display_name"] = display_name
        return self

    def set_display_density(self, display_density):
        self.header["display_density"] = display_density
        return self

    def set_density_dpi(self, density_dpi):
        self.header["density_dpi"] = density_dpi
        return self

    def set_idfa(self, idfa):
        self.header["idfa"] = idfa
        return self

    def set_install_id(self, install_id):
        self.header["install_id"] = install_id
        return self

    def set_language(self, language):
        self.header["language"] = language
        return self

    def set_openudid(self, openudid):
        self.header["openudid"] = openudid
        return self

    def set_os(self, os):
        self.header["os"] = os
        return self

    def set_os_api(self, os_api):
        self.header["os_api"] = os_api
        return self

    def set_os_version(self, os_version):
        self.header["os_version"] = os_version
        return self

    def set_package(self, package):
        self.header["package"] = package
        return self

    def set_region(self, region):
        self.header["region"] = region
        return self

    def set_sdk_version(self, sdk_version):
        self.header["sdk_version"] = sdk_version
        return self

    def set_udid(self, udid):
        self.header["udid"] = udid
        return self

    def set_user_unique_id(self, user_unique_id):
        self.header["user_unique_id"] = user_unique_id
        return self
