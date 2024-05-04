from .target import TargetProxy
from ..client import RshipExecClient
from ..models import Emitter

class EmitterArgs():
  def __init__(self, name: str, short_id: str):
    self.name = name
    self.short_id = short_id

class EmitterProxy():
  def __init__(self, target_proxy: TargetProxy, args: EmitterArgs, client: RshipExecClient):
    self.target = target_proxy
    self.args = args
    self.client = client

  async def save(self):
    emitter = Emitter(
      id=self.id,
      name=self.name,
      schema=self.schema,
      target_id=self.targetId,
      service_id=self.serviceId
    )
    if emitter.id not in self.client.emitters or self.client.emitters[emitter.id].hash != emitter.hash:
      await self.client.set_data(emitter, 'Emitter')

  def id(self) -> str:
    return f"{self.target.instance.args.service_id}:{self.target.args.short_id}:{self.args.short_id}"
  
  async def pule(self, data: any):
    self.client.pulse_emitter(
      self.target.instance.args.service_id, 
      self.target.args.short_id,
      self.args.short_id,
      data,
    )