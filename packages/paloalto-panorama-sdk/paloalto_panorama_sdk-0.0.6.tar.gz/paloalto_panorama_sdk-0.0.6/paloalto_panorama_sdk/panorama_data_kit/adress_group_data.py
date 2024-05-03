import json
from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class AddressGroup:
    location: str
    name: str
    description: str
    static: 'Members'

    @dataclass
    class Members:
        member: List[str]

    def to_json(self):
        data_dict = asdict(self)
        data_dict['@location'] = data_dict.pop('location')
        data_dict['@name'] = data_dict.pop('name')
        if 'static' in data_dict and data_dict['static'] is not None:
            data_dict['static'] = {'member': data_dict.pop('static')}
        return json.dumps(data_dict, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_data: Dict):
        location = json_data.get('@location')
        name = json_data.get('@name')
        description = json_data.get('description')
        static = json_data.get('static', {}).get('member')
        return cls(location, name, description, static)
