"""
Copyright 2020 Beijing Volcano Engine Technology Co., Ltd.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
Apache License, Version 2.0
Home page of The Apache Software Foundation
"""

import json
import logging
import logging.handlers
import queue
from concurrent.futures.thread import ThreadPoolExecutor
import requests
from datarangers.collector.util import constants
from requests.adapters import HTTPAdapter

from datarangers.collector.model.message import Message
from datarangers.collector.writer.writer import RangersWriter


class DataRangersSdkConfig:
    def __init__(self):
        self.__http_header = {
            "Content-Type": "application/json",
            "content-encoding": "gzip",
            "User-Agent": constants.SDK_VERSION
        }
        self.__log_max_bytes = 100 * 1024 * 1024
        self.__log_file_path = "logs/datarangers/"
        self.__log_file_name = "datarangers"
        self.__queue_len = 20480
        self.__send_thread_count = 4
        self.__save = True
        self.__send = False
        self.__http_timeout = 3
        self.sdk_logger = None
        self.sdk_error_logger = None
        self.ready = False

    def is_ready(self):
        return self.ready

    def set_http_header(self, header: dict):
        self.__http_header.update(header)

    def get_http_header(self):
        return self.__http_header

    def set_http_timeout(self, http_timeout: int = 3):
        self.__http_timeout = http_timeout

    def get_http_time_out(self):
        return self.__http_timeout

    def set_domain(self, domain: str):
        self.__domain = domain[0:-1] if domain.endswith("/") else domain
        self.__applog = "{}{}".format(self.__domain, "/sdk/log")
        self.__profile = "{}{}".format(self.__domain, "/data/app/importprofile")

    def get_domain(self):
        return self.__domain

    def get_applog(self):
        return self.__applog

    def get_profile(self):
        return self.__profile

    def enable_save(self):
        self.__save = True
        self.__send = False

    def is_save(self):
        return self.__save

    def enable_send(self):
        self.__save = False
        self.__send = True

    def is_send(self):
        return self.__send

    def set_log_max_bytes(self, log_max_bytes):
        self.__log_max_bytes = log_max_bytes

    def get_log_max_bytes(self):
        return self.__log_max_bytes

    def set_log_file_path(self, log_file_path: str = "logs/datarangers/"):
        self.__log_file_path = log_file_path if log_file_path.endswith("/") else "{}/".format(log_file_path)

    def get_log_file_path(self):
        return self.__log_file_path

    def set_log_file_name(self, log_file_name: str = "datarangers.log"):
        self.__log_file_name = log_file_name

    def get_log_file_name(self):
        return self.__log_file_name

    def set_queue_length(self, queue_len: int):
        self.__queue_len = queue_len

    def get_queue_length(self):
        return self.__queue_len

    def set_send_thread_count(self, thread_count: int):
        self.__send_thread_count = thread_count

    def get_send_thread_count(self):
        return self.__send_thread_count

    def init(self, config: dict):
        if not self.is_ready():
            self.set_http_header(config.get("headers", {
                "Content-Type": "application/json",
                "content-encoding": "gzip",
                "User-Agent": constants.SDK_VERSION
            }))
            self.set_http_timeout(config.get("http_timeout", 3))
            self.set_domain(config.get("domain", "http://127.0.0.1"))
            if "save" in config:
                if config.get("save"):
                    self.enable_save()
                else:
                    self.enable_send()
            self.set_log_max_bytes(config.get("log_max_bytes", 100 * 1024))
            self.set_log_file_name(config.get("log_file_name", "datarangers"))
            self.set_log_file_path(config.get("log_file_path", "logs/datarangers/"))
            self.set_queue_length(config.get("queue_length", 20480))
            self.set_send_thread_count(config.get("thread_count", 4))

            self.sdk_logger = RangersWriter(self.get_log_file_path(), self.get_log_file_name(),
                                            self.get_log_max_bytes())
            self.sdk_error_logger = RangersWriter(self.get_log_file_path(), "{}-error".format(self.get_log_file_name()),
                                                  self.get_log_max_bytes())
            if self.is_send():
                self.sdk_queue = queue.Queue(maxsize=self.get_queue_length())
                self.__sdk_executor = ThreadPoolExecutor(max_workers=self.get_send_thread_count())
                for i in range(self.get_send_thread_count()):
                    self.__sdk_executor.submit(DataRangersSdkConfig.consumer_thread,
                                               "datarangers-consumer-{}".format(i),
                                               self.sdk_queue)
            self.ready = True

    @staticmethod
    def consumer_thread(name, t_queue: queue.Queue):
        session = requests.Session()
        session.mount('http://', HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=3))
        session.mount('https://', HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=3))
        logging.debug("成功启动消费者-{}".format(name))
        while True:
            try:
                msg = t_queue.get(block=True)
                if msg and dataRangersSdkConfig.is_send():
                    logging.debug(msg.get_json())
                    if type(msg) == Message:
                        try:
                            res = session.post(dataRangersSdkConfig.get_applog(),
                                               headers=dataRangersSdkConfig.get_http_header(),
                                               data=msg.get_json(), timeout=dataRangersSdkConfig.get_http_time_out())
                            result = json.loads(res.content)
                            logging.info(result)
                            if "message" not in result or result["message"] != "success":
                                logging.error("Send Error")
                                dataRangersSdkConfig.sdk_error_logger.debug(msg.get_json())
                        except Exception as e:
                            logging.error(e)
                            dataRangersSdkConfig.sdk_error_logger.debug(msg.get_json())
                    else:
                        continue
                else:
                    dataRangersSdkConfig.sdk_error_logger.info(msg.get_json())

            except:
                break
        logging.info("消费者-{}退出".format(name))


dataRangersSdkConfig = DataRangersSdkConfig()
