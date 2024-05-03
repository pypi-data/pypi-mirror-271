import json
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class ServiceGroup:
    location: str
    name: str
    members: 'Members'

    @dataclass
    class Members:
        member: List[str]

    def to_json(self):
        data_dict = asdict(self)
        data_dict['@location'] = data_dict.pop("location")
        data_dict['@name'] = data_dict.pop("name")
        return json.dumps(data_dict, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_data):
        location = json_data.get('@location')
        name = json_data.get('@name')
        members = {"member": json_data.get('members', {}).get('member')}
        return cls(location, name, members)
