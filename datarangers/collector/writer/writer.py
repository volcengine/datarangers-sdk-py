"""
Copyright 2020 Beijing Volcano Engine Technology Co., Ltd.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
Apache License, Version 2.0
Home page of The Apache Software Foundation
"""
import os, datetime
import random


class RangersWriter:
    def __init__(self, log_file_path: str, log_file_name: str, max_size=1024 * 1024 * 1):
        self.prefix = log_file_path
        if log_file_name.endswith(".log"):
            log_file_name = log_file_name[0:-4]
        self.file_name = "{}-{}{}".format(log_file_name, datetime.datetime.now().strftime("%Y-%m-%d-%H"), ".log")
        self.write_name = os.path.join(self.prefix, "{}.log".format(log_file_name))
        self.full_name = os.path.join(self.prefix, self.file_name)
        self.name = log_file_name
        self.max_size = max_size
        self.index = 0
        self.get_index()
        self.index += 1
        self.__writer = open(self.write_name, "a")
        self.current_count = 0

    def check_size(self):
        size = os.path.getsize(self.write_name)
        if size > self.max_size:
            self.change_file_name()

    def change_file_name(self):
        target_name = "{}.{}".format(self.full_name, self.index)
        self.__writer.flush()
        self.__writer.close()
        os.rename(self.write_name, target_name)
        self.index += 1
        self.__writer = open(self.write_name, "a+")

    def get_index(self):
        if not os.path.exists(self.prefix):
            os.makedirs(self.prefix)
            return
        for path in os.listdir(self.prefix):
            if not os.path.isdir(path):
                if self.file_name in path and not path.endswith(".log"):
                    self.index = max(self.index, int(path.replace("{}.".format(self.file_name), "")))

    """
    如果不及时flush,进程崩溃的情况下数据会丢失
    """
    def info(self, message):
        self.__writer.write("{}\n".format(message))
        if self.current_count > 20000:
            self.__writer.flush()
            self.check_size()

    def debug(self, message):
        self.info(message)

    def __del__(self):
        self.__writer.close()


if __name__ == "__main__":
    rangers = RangersWriter("./logs", "sensor")
    for i in range(1000000):
        rangers.info("--214adfwfewa")
