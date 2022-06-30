# DataRangers

## 项目背景
datarangers-sdk-php是 [DataRangers](https://datarangers.com.cn/) 的用户行为采集服务端SDK。

服务端埋点支持在客户的服务端进行埋点采集和上报，作为客户端埋点的补充或替代，其支持的典型场景包括：
1. 客户端埋点+服务端埋点组合：该场景下，服务端埋点一般用来弥补客户端埋点覆盖不到的部分数据，是目前最常见的使用场景。
2. 纯服务端埋点：所有的埋点收集和上报都由服务端完成，需要的客户端数据则由服务端收集和提取后上报到DataRangers。

## 使用方法
1. 按照SDK
2. 初始化SDK
    ```python
       EventCollector.init(
            {
                "headers": {
                    "Host": "host"
                },
                "http_timeout": 0.2,
                "domain": "http://127.0.0.1",
                "save": False,
                "log_max_bytes": 100 * 1024,
                "log_file_name": "datarangers",
                "log_file_path": "logs/datarangers/",
                "queue_length": 204800,
                "thread_count": 4
            }
        )
    ```
    参数说明
    * Http模式
        * headers：http的header，需要设置Host
        * http_timeout： http的超时时间，单位为秒
        * domain： http的发送域名，请使用私有化SDK配置的域名
        * save： False，Http模式需要设置为False
        * queue_length： 队列的长度，需要进行合理配置，保证生产的速度不会将队列填满
        * thread_count： 发送的线程数量
    * LogAgent模式
        * save： True
        * log_max_bytes： 保存的日志的最大大小
        * log_file_name： 保存的日志的文件名
        * log_file_path： 保存的日志的路径
        * queue_length： 队列的长度，需要进行合理配置，保证生产的速度不会将队列填满
    
3. 上报事件接口
    ```python
    @staticmethod
    def send_app_event(user_unique_id: str, app_id: int, custom: dict, event_name, event_params,
                       device_type=None, device_uniq_id=None, ab_sdk_version=None):
        r""" send app event

        :param user_unique_id: uuid
        :param app_id: app id
        :param custom
        :param event_name,event_params,ab_sdk_version
            if isinstance(event_name, str):
                isinstance(event_params,dict) -> event_params should be a dict
            else if isinstance(event_name, list):
                isinstance(event_params,list) and len(event_params) == len(event_name)
                which mean event_name[n]'s params is event_params[n],
                ab_sdk_version[n]'s params is ab_sdk_version[n]
        :param device_type: ["android","ios"]
        :param device_uniq_id: device identification
        :param ab_sdk_version: ab_sdk_version
        """
     
    @staticmethod
    def send_mp_event(user_unique_id: str, app_id: int, custom: dict, event_name, event_params,
                      device_uniq_id=None, ab_sdk_version=None):
        r""" send mp event

        :param user_unique_id: uuid
        :param app_id: app id
        :param custom
        :param event_name,event_params,ab_sdk_version
            if isinstance(event_name, str):
                isinstance(event_params,dict) -> event_params should be a dict
            else if isinstance(event_name, list):
                isinstance(event_params,list) and len(event_params) == len(event_name)
                which mean event_name[n]'s params is event_params[n],
                ab_sdk_version[n]'s params is ab_sdk_version[n]
        :param device_uniq_id: device identification
        :param ab_sdk_version: ab_sdk_version
        """
     
    @staticmethod
    def send_web_event(user_unique_id: str, app_id: int, custom: dict, event_name, event_params,
                      device_uniq_id=None, ab_sdk_version=None):
        r""" send web event

        :param user_unique_id: uuid
        :param app_id: app id
        :param custom
        :param event_name,event_params, ab_sdk_version
            if isinstance(event_name, str):
                isinstance(event_params,dict) -> event_params should be a dict
            else if isinstance(event_name, list):
                isinstance(event_params,list) and len(event_params) == len(event_name)
                which mean event_name[n]'s params is event_params[n],
                ab_sdk_version[n]'s params is ab_sdk_version[n]

        :param device_uniq_id: device identification
        :param ab_sdk_version: ab_sdk_version
        """
     
    @staticmethod
    def profile_set(user_unique_id: str, app_id: int, event_params):
        r""" send app event
    
        :param user_unique_id: uuid
        :param app_id: app id
        :param event_params: dict, set user profile
        """
    
    @staticmethod
    def profile_unset(user_unique_id: str, app_id: int, event_params: list):
        r""" send app event
    
        :param user_unique_id: uuid
        :param app_id: app id
        :param event_params: list, unset user profile
        """
        
    @staticmethod
    def profile_set_once(user_unique_id: str, app_id: int, event_params):
        r""" send app event
    
        :param user_unique_id: uuid
        :param app_id: app id
        :param event_params: dict, set only once user profile
        """   
        
    @staticmethod
    def profile_increment(user_unique_id: str, app_id: int, event_params):
        r""" send app event
    
        :param user_unique_id: uuid
        :param app_id: app id
        :param event_params: dict
            params's value should be integer
        """  
    @staticmethod
    def profile_append(user_unique_id: str, app_id: int, event_params):
        r""" send app event
    
        :param user_unique_id: uuid
        :param app_id: app id
        :param event_params: dict
            params's value should be list of string
        """
    
    @staticmethod
    def item_set(app_id: int, name, items_params: list):
        r"""send item set event
    
        :param app_id: app id
        :param name: item_name
        :param items_params:list of dict
            list of items: item should be a dict, item_name and item_value are necessary
        """
    
    @staticmethod
    def item_unset(app_id: int, id, name, item_params: list):
        r""" unset item
    
        :param app_id: app id
        :param name: item_name
        :param item_params:list
        """
    
    ```
    发送事件
    ```python
    EventCollector.send_mp_event("uuid", 10000014, None, "test_event_test_new_py",
                             {"date_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    ```
    设置用户profile
    ```python
    EventCollector.profile_set(10000013,"book",{"name":"name","age":12})
     ```
   设置item事件
   ```python
    EventCollector.item_set(10000013,"book",[{"id": "0001","item_name": "book","price":100.0}])
   ```
   
   
   
   
## License
Copyright 2020 Beijing Volcano Engine Technology Co., Ltd.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. 
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
