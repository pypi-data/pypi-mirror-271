from ..models import Target, TargetStatus, TargetStatusEnum
from ..client import RshipExecClient

class TargetArgs():
    def __init__(self, name: str, short_id: str, category: str):
        self.name = name
        self.short_id = short_id
        self.category = category

class TargetProxy():
    def __init__(self, instance, args: TargetArgs, client: RshipExecClient):
        self.instance = instance
        self.args = args
        self.client = client

    # async def add_emitter(self, args: EmitterArgs):
    #    return    

    # async def add_action(self, args: EmitterArgs):
    #    return

    async def save(self, status: TargetStatusEnum):
        target = Target(
          name=self.args.name,
          id=self.id(),
          category=self.args.category,
          bg_color=self.instance.args.color,
          fg_color=self.instance.args.color,
          parent_targets=[],
          sub_targets=[],
          service_id=self.instance.args.service_id,
          root_level=True,
          # hash=generate_hash(),
        )

        status = TargetStatus(
            id=f"{self.instance.args.service_id}:{self.args.short_id}",
            target_id=self.id(),
            status=status,
            instance_id=self.instance.args.short_id,
            # hash=generate_hash()
        )

    def id(self) -> str:
        return f"{self.instance.args.service_id}:{self.args.short_id}"
    
    async def set_status(self, status: TargetStatusEnum):
        await self.save(status)