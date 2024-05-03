import asyncio
import json
import websockets
from typing import Any, Callable, Dict
from myko import MEvent, MEventType, MCommand, WSMEvent, WSMCommand
from .models import Target, Action, Emitter, Pulse, Instance, Machine, Alert, InstanceStatusEnum, TargetStatus, TargetStatusEnum, AlertEntityType, AlertLevel
from .utils import generate_id, get_current_timestamp, make_instance_id

class RshipExecClient:
    def __init__(self, rship_host: str, rship_port: int):
        self.rship_host = rship_host
        self.rship_port = rship_port
        self.is_connected = False
        self.client_id = None
        self.websocket = None
        self.targets: Dict[str, Target] = {}
        self.actions: Dict[str, Action] = {}
        self.emitters: Dict[str, Emitter] = {}
        self.instances: Dict[str, Instance] = {}
        self.machines: Dict[str, Machine] = {}
        self.alerts: Dict[str, Alert] = {}
        self.handlers: Dict[str, Callable[[Action, Any], None]] = {}

    async def connect(self):
        uri = f"ws://{self.rship_host}:{self.rship_port}/myko"
        print(f"Attempting to connect to {uri}")
        try:
            self.websocket = await websockets.connect(uri)
            print("Connected to Rship server successfully.")
            self.is_connected = True
        except Exception as e:
            print(f"Failed to connect: {e}")

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            print("Disconnected from Rship server")
            self.is_connected = False

    async def send_event(self, event: MEvent):
        if self.websocket:
            await self.websocket.send(json.dumps(WSMEvent(event).__dict__))

    async def send_command(self, command: MCommand):
        if self.websocket:
            await self.websocket.send(json.dumps(WSMCommand(command).__dict__))

    async def receive_messages(self):
        while self.websocket:
            try:
                message = await self.websocket.recv()
                await self.handle_message(message)
            except websockets.ConnectionClosed:
                await self.disconnect()

    async def handle_message(self, message: str):
        data = json.loads(message)
        if data["event"] == "ws:m:command":
            command_data = data["data"]
            command_id = command_data["commandId"]
            if command_id == "client:setId":
                self.client_id = command_data["command"]["clientId"]
                print(f"Received client ID: {self.client_id}")
            elif command_id == "target:action:exec":
                action_id = command_data["command"]["action"]["id"]
                if action_id in self.actions:
                    action = self.actions[action_id]
                    handler = self.handlers.get(action_id)
                    if handler:
                        handler(action, command_data["command"]["data"])

    def set_handler(self, action_id: str, handler: Callable[[Action, Any], None]):
        self.handlers[action_id] = handler

    def remove_handler(self, action_id: str):
        if action_id in self.handlers:
            del self.handlers[action_id]

    async def set_data(self, item: Any, item_type: str):
        event = MEvent(item=item, item_type=item_type, change_type=MEventType.SET,
                       created_at=get_current_timestamp(), tx=generate_id())
        await self.send_event(event)

    async def delete_data(self, item: Any):
        event = MEvent(item=item, item_type=type(item).__name__, change_type=MEventType.DEL,
                       created_at=get_current_timestamp(), tx=generate_id())
        await self.send_event(event)

    async def pulse_emitter(self, emitter_id: str, data: Any):
        pulse = Pulse(id=generate_id(), name="", emitter_id=emitter_id, data=data)
        await self.set_data(pulse, 'Pulse')

    async def set_instance_offline(self, instance_id: str):
        instance = self.instances.get(instance_id)
        if instance:
            instance.status = InstanceStatus.UNAVAILABLE
            await self.set_data(instance, 'Instance')

    async def set_target_offline(self, target_id: str, instance_id: str):
        target = self.targets.get(target_id)
        if target:
            await self.set_target_status(target_id, instance_id, TargetStatus.OFFLINE)

    async def set_target_status(self, target_id: str, instance_id: str, status: TargetStatus):
        target_status = TargetStatus(id=f"{instance_id}:{target_id}", target_id=target_id,
                                     instance_id=instance_id, status=status)
        await self.set_data(target_status, 'TargetStatus')

    async def save_machine(self, machine: Machine):
        self.machines[machine.id] = machine
        await self.set_data(machine, 'Machine')

    async def save_instance(self, instance: Instance):
        self.instances[instance.id] = instance
        await self.set_data(instance, 'Instance')

    async def save_target(self, target: Target):
        self.targets[target.id] = target
        await self.set_data(target, 'Target')

    async def save_action(self, action: Action):
        self.actions[action.id] = action
        await self.set_data(action, 'Action')

    async def save_emitter(self, emitter: Emitter):
        self.emitters[emitter.id] = emitter
        await self.set_data(emitter, 'Emitter')

    def save_handler(self, action_id: str, handler: Callable[[Action, Any], None]):
        self.handlers[action_id] = handler