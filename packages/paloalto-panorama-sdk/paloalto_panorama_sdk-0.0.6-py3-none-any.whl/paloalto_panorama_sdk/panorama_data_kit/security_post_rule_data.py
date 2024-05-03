import json
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class SecurityPostRule:
    name: str
    uuid: str
    location: str
    device_group: str
    loc: str
    description: str
    action: str
    log_settings: str
    from_member: 'Members'
    to_member: 'Members'
    source_member: 'Members'
    destination_member: 'Members'
    service_member: 'Members'
    application_member: 'Members'
    tag_member: 'Members'
    profile_setting: 'Members'

    @dataclass
    class Members:
        member: List[str]

    @dataclass
    class ProfileSettingMembers:
        group: 'SecurityPostRule.Members'

    def to_json(self):
        data_dict = asdict(self)
        data_dict['@name'] = data_dict.pop("name")
        data_dict['@uuid'] = data_dict.pop("uuid")
        data_dict['@location'] = data_dict.pop("location")
        data_dict['@device-group'] = data_dict.pop("device_group")
        data_dict['@loc'] = data_dict.pop("loc")
        return json.dumps(data_dict, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_data):
        name = json_data.get('@name')
        uuid = json_data.get('@uuid')
        location = json_data.get('@location')
        device_group = json_data.get('@device-group')
        loc = json_data.get('@loc')
        description = json_data.get('description')
        action = json_data.get('action')
        log_settings = json_data.get('log-settings')
        from_member = json_data.get("from", {}).get('member')
        to_member = json_data.get("to", {}).get('member')
        source_member = json_data.get("source", {}).get('member')
        destination_member = json_data.get("destination", {}).get('member')
        service_member = json_data.get("service", {}).get('member')
        application_member = json_data.get("application", {}).get('member')
        tag_member = json_data.get("tag", {}).get('member')
        profile_setting = json_data.get("profile-setting", {}).get('member')
        return cls(name, uuid, location, device_group, loc, description, action, log_settings,
                   from_member, to_member, source_member, destination_member, service_member,
                   application_member, tag_member, profile_setting)
