from metagpt.roles import Role
from metagpt.actions import Action
from metagpt.logs import logger
from metagpt.team import Message
import subprocess

from agents.main_control_agent import BuildPlan

class BuildCode(Action):
    name: str = "BuildCode"

    async def run(self):
        result = subprocess.run(["python", "-c", "print('Build code command placeholder')"], capture_output=True, text=True).stdout
        logger.info(f"{result=}")
        return result
    

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

        result = await todo.run()

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
