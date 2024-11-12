from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.team import Message

from agents.actions import BuildPlan, BuildCode

class BuildAgent(Role):
    name: str = "Build Agent"
    profile: str = "Handles building pull requests"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([BuildCode])
        self._watch([BuildPlan])

    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        context = self.get_memories()[-1].content

        result = await todo.run(context)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
