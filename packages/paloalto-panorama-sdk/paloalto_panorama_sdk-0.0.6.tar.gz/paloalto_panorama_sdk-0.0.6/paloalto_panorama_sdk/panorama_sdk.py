import os
from pprint import pprint

from paloalto_panorama_sdk.address_groups_manager import AddressGroupsManager
from paloalto_panorama_sdk.address_manager import AddressManager
from paloalto_panorama_sdk.key_manager import KeyManager
from paloalto_panorama_sdk.panorama_data_kit.adress_data import Address
from paloalto_panorama_sdk.panorama_data_kit.adress_group_data import AddressGroup
from paloalto_panorama_sdk.panorama_data_kit.security_post_rule_data import SecurityPostRule
from paloalto_panorama_sdk.panorama_data_kit.service_data import Service
from paloalto_panorama_sdk.panorama_data_kit.service_group_data import ServiceGroup
from paloalto_panorama_sdk.security_post_rules_manager import SecurityPostRulesManager
from paloalto_panorama_sdk.service_groups_manager import ServiceGroupsManager
from paloalto_panorama_sdk.service_manager import ServiceManager
from dotenv import load_dotenv

load_dotenv()


class PanoramaSDK:
    def __init__(self, url, username, password, verify=True):
        self.url = url
        self.username = username
        self.password = password
        self.apikey = KeyManager.get_api_key(
            panorama_url=self.url,
            user=self.username,
            password=self.password,
            verify=verify
        )
        self.address_group = AddressGroupsManager(panorama_url=self.url, api_key=self.apikey, verify=verify)
        self.address = AddressManager(panorama_url=self.url, api_key=self.apikey, verify=verify)
        self.security_post_rule = SecurityPostRulesManager(panorama_url=self.url, api_key=self.apikey, verify=verify)
        self.service_group = ServiceGroupsManager(panorama_url=self.url, api_key=self.apikey, verify=verify)
        self.service = ServiceManager(panorama_url=self.url, api_key=self.apikey, verify=verify)


if __name__ == '__main__':
    panSDK = PanoramaSDK(
        url=os.getenv("url", ""),
        username=os.getenv("user", "test"),
        password=os.getenv("password", "testpass"),
        verify=False
    )
    serOutput = panSDK.service.list_services()
    se = Service.from_json(serOutput['result']['entry'][0])
    pprint(serOutput)
    print(se)
    pprint(se.to_json())
