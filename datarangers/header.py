class Header:
    def __init__(self, ab_client: str = None,
                 ab_sdk_version: str = None,
                 ab_version: str = None,
                 app_id: int = None, app_name: str = None,
                 app_channel: str = None,
                 app_install_id: int = None,
                 app_language: str = None,
                 app_package: str = None,
                 app_region: str = None,
                 app_version: str = None,
                 browser: str = None, browser_version: str = None,
                 campaign_id: int = None,
                 carrier: str = None,
                 carried_region: str = None,
                 city: str = None,
                 client_ip: str = None,
                 custom: dict = None,
                 device_brand: str = None,
                 device_model: str = None,
                 language: str = None,
                 os_name: str = None,
                 os_version: str = None,
                 platform: str = None,
                 province: str = None,
                 referrer_host: str = None,
                 region: str = None,
                 resolution: str = None,
                 screen_height: int = None,
                 screen_width: int = None):
        self.ab_client = ab_client
        self.ab_sdk_version = ab_sdk_version
        self.ab_version = ab_version
        self.app_id = app_id
        self.aid = app_id
        self.app_name = app_name
        self.app_channel = app_channel
        self.app_install_id = app_install_id
        self.app_language = app_language
        self.app_package = app_package
        self.app_region = app_region
        self.app_version = app_version
        self.browser = browser
        self.browser_version = browser_version
        self.campaign_id = campaign_id
        self.carrier = carrier
        self.carried_region = carried_region
        self.city = city
        self.client_ip = client_ip
        self.custom = custom
        self.device_brand = device_brand
        self.device_model = device_model
        self.language = language
        self.os_name = os_name
        self.os_version = os_version
        self.platform = platform
        self.province = province
        self.referrer_host = referrer_host
        self.region = region
        self.resolution = resolution
        self.screen_height = screen_height
        self.screen_width = screen_width

    def set_ab_client(self, ab_client):
        self.ab_client = ab_client
        return self

    def set_ab_sdk_version(self, ab_sdk_version):
        self.ab_sdk_version = ab_sdk_version
        return self

    def set_ab_version(self, ab_version):
        self.ab_version = ab_version
        return self

    def set_app_id(self, app_id):
        self.app_id = app_id
        self.aid = app_id
        return self

    def set_app_name(self, app_name):
        self.app_name = app_name
        return self

    def set_app_channel(self, app_channel):
        self.app_channel = app_channel
        return self

    def set_app_install_id(self, app_install_id):
        self.app_install_id = app_install_id
        return self

    def set_app_language(self, app_language):
        self.app_language = app_language
        return self

    def set_app_package(self, app_package):
        self.app_package = app_package
        return self

    def set_app_region(self, app_region):
        self.app_region = app_region
        return self

    def set_app_version(self, app_version):
        self.app_version = app_version
        return self

    def set_browser(self, browser):
        self.browser = browser
        return self

    def set_browser_version(self, browser_version):
        self.browser_version = browser_version
        return self

    def set_carrier(self, carrier):
        self.carrier = carrier
        return self

    def set_carried_region(self, carried_region):
        self.carried_region = carried_region
        return self

    def set_city(self, city):
        self.city = city
        return self

    def set_client_ip(self, client_ip):
        self.client_ip = client_ip
        return self

    def set_custom(self, custom):
        self.custom = custom
        return self

    def set_device_brand(self, device_brand):
        self.device_brand = device_brand
        return self

    def set_device_model(self, device_model):
        self.device_model = device_model
        return self

    def set_language(self, language):
        self.language = language
        return self

    def set_os_name(self, os_name):
        self.os_name = os_name
        return self

    def set_os_version(self, os_version):
        self.os_version = os_version
        return self

    def set_platform(self, platform):
        self.platform = platform
        return self

    def set_province(self, province):
        self.province = province
        return self

    def set_referrer_host(self, referrer_host):
        self.referrer_host = referrer_host
        return self

    def set_region(self, region):
        self.region = region
        return self

    def set_resolution(self, resolution):
        self.resolution = resolution
        return self

    def set_screen_height(self, screen_height):
        self.screen_height = screen_height
        return self

    def set_screen_width(self, screen_width):
        self.screen_width = screen_width
        return self
