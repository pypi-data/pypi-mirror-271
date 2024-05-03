# Palo Alto - Panorama SDK

This project serves as an SDK for Palo Alto Panorama.  
This should allow easier access to the Panorama API.  
The project is currently still at a very early stage.

## Install
```
pip install paloalto-panorama-sdk
```

## Example



```
import os
from paloalto_panorama_sdk.panorama_sdk import PanoramaSDK


if __name__ == '__main__':
    panSDK = PanoramaSDK(
        url=os.getenv("url", "127.0.0.1:5000"),
        username=os.getenv("username", "testuser"),
        password=os.getenv("password", "testpassword")
    )
    print(panSDK.service.list_services())
    print(panSDK.security_post_rules.list_post_rules())
    print(panSDK.address_groups.list_address_groups())
```

It is currently available on https://pypi.org/project/paloalto-panorama-sdk/ and soon on gitlab.com 