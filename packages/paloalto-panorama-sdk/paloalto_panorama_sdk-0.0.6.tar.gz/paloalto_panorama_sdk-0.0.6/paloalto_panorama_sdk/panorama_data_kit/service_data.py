import json
from dataclasses import dataclass, asdict


@dataclass
class Service:
    location: str
    name: str
    description: str
    protocol: 'Protocol'

    @dataclass
    class Protocol:
        protocol: str
        port: str

    def to_json(self):
        data_dict = asdict(self)
        data_dict['@location'] = data_dict.pop("location")
        data_dict['@name'] = data_dict.pop("name")
        return json.dumps(data_dict, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_data):
        location = json_data.get('@location')
        name = json_data.get('@name')
        description = json_data.get('description')
        protocol = json_data.get('protocol')
        return cls(location, name, description, protocol)
