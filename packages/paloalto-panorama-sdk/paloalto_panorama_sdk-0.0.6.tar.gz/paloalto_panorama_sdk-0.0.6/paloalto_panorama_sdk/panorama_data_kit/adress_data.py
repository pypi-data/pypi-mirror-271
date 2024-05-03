import json
from dataclasses import dataclass, asdict


@dataclass
class Address:
    location: str
    name: str
    description: str
    ip_netmask: str

    def to_json(self):
        data_dict = asdict(self)
        data_dict['@location'] = data_dict.pop('location')
        data_dict['@name'] = data_dict.pop('name')
        data_dict['ip-netmask'] = data_dict.pop('ip_netmask')
        return json.dumps(data_dict, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_data):
        location = json_data['@location']
        name = json_data.get('@name')
        description = json_data.get('@description')
        ip_netmask = json_data.get('ip-netmask')
        return cls(location, name, description, ip_netmask)
