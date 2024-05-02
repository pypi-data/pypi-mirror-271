from enum import Enum
from typing import List, Optional, Any, Callable
from myko import MItem, MCommand, Schema

class Target(MItem):
    def __init__(self, id: str, name: str, action_ids: List[str], emitter_ids: List[str],
                 sub_targets: List[str], parent_targets: List[str], service_id: str,
                 bg_color: str, fg_color: str, last_updated: str, category: str, root_level: bool):
        super().__init__(id, name)

        self.action_ids = action_ids
        self.emitter_ids = emitter_ids
        self.sub_targets = sub_targets
        self.parent_targets = parent_targets
        self.service_id = service_id
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.last_updated = last_updated
        self.category = category
        self.root_level = root_level


class Status(Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'


class TargetStatus(MItem):
    def __init__(self, id: str, name: str, targetId: str, status: Enum, lastUpdated: str, instanceId: str):
        super().__init__(id, name)

        self.targetId = targetId
        self.status = status.value
        self.lastUpdated = lastUpdated
        self.instanceId = instanceId


class Action(MItem):
    def __init__(self, id: str, name: str, schema: Optional[Schema], target_id: str, service_id: str):
        super().__init__(id, name)

        self.schema = schema
        self.target_id = target_id
        self.service_id = service_id


class Emitter(MItem):
    def __init__(self, id: str, name: str, schema: Optional[Schema], target_id: str, service_id: str):
        super().__init__(id, name)

        self.schema = schema
        self.target_id = target_id
        self.service_id = service_id


class Pulse(MItem):
    def __init__(self, id: str, name: str, emitter_id: str, data: Any):
        super().__init__(id, name)

        self.emitter_id = emitter_id
        self.data = data


class InstanceStatus(Enum):
    STARTING = 'Starting'
    AVAILABLE = 'Available'
    STOPPING = 'Stopping'
    UNAVAILABLE = 'Unavailable'
    ERROR = 'Error'


class Instance(MItem):
    def __init__(self, id: str, name: str, service_id: str, client_id: str, service_type_code: str,
                 status: InstanceStatus, machine_id: str, color: str):
        super().__init__(id, name)

        self.service_id = service_id
        self.client_id = client_id
        self.service_type_code = service_type_code
        self.status = status.value
        self.machine_id = machine_id
        self.color = color


class Machine(MItem):
    name: str
    dnsName: str
    execName: str
    address: str

    def __init__(self, name: str):
        super().__init__(name, name)

        self.name = name
        self.dns_name = name
        self.exec_name = name
        self.address = 'fakeAddress'


class Service(MItem):
    def __init__(self, id: str, name: str, systemTypeCode: str):
        super().__init__(id, name)

        self.systemTypeCode = systemTypeCode


class ExecTargetAction(MCommand):
    def __init__(self, tx: str, createdAt: str, action: Action, data: any):
        super().__init__(tx, createdAt)

        self.action = action
        self.data = data


class AlertLevel(Enum):
    INFO = 'info'
    WARN = 'warn'
    ERROR = 'error'


class AlertEntityType(Enum):
    TARGET = 'Target'
    ACTION = 'Action'
    PAYLOAD = 'Payload'
    INSTANCE = 'Instance'


class Alert(MItem):
    def __init__(self, id: str, entity_id: str, entity_type: AlertEntityType, instance_id: str,
                 level: AlertLevel, message: str, code: str):
        super().__init__(id, f"{entity_id}:{code}")
        self.entity_id = entity_id
        self.entity_type = entity_type.value
        self.instance_id = instance_id
        self.level = level.value
        self.message = message
        self.code = code


class ActionProps:
    def __init__(self, id: str, name: str, schema: Optional[Schema], handler: Callable[[Any], None]):
        self.id = id
        self.name = name
        self.schema = schema
        self.handler = handler


class EmitterProps:
    def __init__(self, id: str, name: str, schema: Optional[Schema]):
        self.id = id
        self.name = name
        self.schema = schema

class AlertProps:
    def __init__(self, message: str, level: str, code: str):
        self.message = message
        self.level = level
        self.code = code


class TargetProps:
    def __init__(self, id: str, name: str, category: str, actions: List[ActionProps],
                 subtargets: List['TargetProps'], parent_targets: List[str],
                 emitters: List[EmitterProps], alerts: List[AlertProps]):
        self.id = id
        self.name = name
        self.category = category
        self.actions = actions
        self.subtargets = subtargets
        self.parent_targets = parent_targets
        self.emitters = emitters
        self.alerts = alerts