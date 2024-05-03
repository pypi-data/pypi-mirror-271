from enum import Enum
from typing import List, Optional, Any, Callable
from myko import MItem, MCommand, Schema

class Target(MItem):
    def __init__(self, id: str, name: str,
                 sub_targets: List[str], parent_targets: List[str], service_id: str,
                 bg_color: str, fg_color: str, last_updated: str, category: str, root_level: bool):
        super().__init__(id, name)

        self.subTargets = sub_targets
        self.parentTargets = parent_targets
        self.serviceId = service_id
        self.bgColor = bg_color
        self.fgColor = fg_color
        self.lastUpdated = last_updated
        self.category = category
        self.rootLevel = root_level


class Status(Enum):
    Online = 'online'
    Offline = 'offline'


class TargetStatus(MItem):
    def __init__(self, name: str, targetId: str, status: Enum, lastUpdated: str, instanceId: str):
        super().__init__(instanceId + targetId, name)

        self.targetId = targetId
        self.status = status.value
        self.lastUpdated = lastUpdated
        self.instanceId = instanceId


class Action(MItem):
    def __init__(self, id: str, name: str, schema: Optional[Schema], target_id: str, service_id: str):
        super().__init__(id, name)

        self.schema = schema
        self.targetId = target_id
        self.serviceId = service_id


class Emitter(MItem):
    def __init__(self, id: str, name: str, schema: Optional[Schema], target_id: str, service_id: str):
        super().__init__(id, name)

        self.schema = schema
        self.targetId = target_id
        self.serviceId = service_id


class Pulse(MItem):
    def __init__(self, id: str, name: str, emitter_id: str, data: Any):
        super().__init__(id, name)

        self.emitterId = emitter_id
        self.data = data


class InstanceStatus(Enum):
    Starting = 'Starting'
    Available = 'Available'
    Stopping = 'Stopping'
    Unavailable = 'Unavailable'
    Error = 'Error'


class Instance(MItem):
    def __init__(self, name: str, service_id: str, client_id: str, service_type_code: str,
                 status: InstanceStatus, machine_id: str, color: str):
        super().__init__(machine_id + service_id, name)

        self.serviceId = service_id
        self.clientId = client_id
        self.serviceTypeCode = service_type_code
        self.status = status.value
        self.machineId = machine_id
        self.color = color


class Machine(MItem):
    name: str
    dnsName: str
    execName: str
    address: str

    def __init__(self, name: str):
        super().__init__(name, name)

        self.name = name
        self.dnsName = name
        self.execName = name
        self.address = 'fakeAddress'

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
    def __init__(self, entity_id: str, entity_type: AlertEntityType, instance_id: str,
                 level: AlertLevel, message: str, code: str):
        super().__init__(entity_id + instance_id, f"{entity_id}:{code}")
        self.entityId = entity_id
        self.entityType = entity_type.value
        self.instanceId = instance_id
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
        self.parentTargets = parent_targets
        self.emitters = emitters
        self.alerts = alerts