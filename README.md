## 服务端埋点Python SDK
1. 设置上报参数
   ```python
   from collector import Collector
   # 选择一种方式设置上报参数
   Collector.set_ip_port("10.225.130.127", 31081)
   Collector.set_urls("10.225.130.127:31081")
   ```
2. 设置上报信息
   ```python
   import time, datetime
   from event import Event
   from header import Header
   from user import User
   user = User(
        user_unique_id='860520117802285'
    )
    header = Header().set_app_id(10000014).set_app_name("app_name").set_app_channel("App Store").set_client_ip(
        "10.225.130.127").set_app_install_id("1234567").set_device_model("Mate30")
    events = [Event().set_event("python_event_test2").set_time(int(time.time())).set_local_time_ms(
        int(time.time() * 1000)).set_session_id("bcb03ea33214b3414f3a148385f08f07483c").set_params(
        {"date_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}),
        Event().set_event("python_event_test3").set_time(int(time.time())).set_local_time_ms(
            int(time.time() * 1000)).set_session_id("bcb03ea33214b3414f3a148385f08f07483c").set_params(
            {"date_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}),
        Event().set_event("python_event_test4").set_time(int(time.time())).set_local_time_ms(
            int(time.time() * 1000)).set_session_id("bcb03ea33214b3414f3a148385f08f07483c").set_params(
            {"date_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})]
   ```
3. 上报
   ```python
   from collector import Collector
   Collector.send_mp_events("2ec5389c5d2de0b63e7a82df28a1a712", user, header, events) # 任意选其一
   Collector.send_app_events("2ec5389c5d2de0b63e7a82df28a1a712", user, header, events)
   ```   
