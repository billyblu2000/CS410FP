from metagpt.roles import Role
from metagpt.actions import Action
from metagpt.logs import logger
from metagpt.team import Message
import subprocess

from agents.main_control_agent import TestPlan

class GenerateAndRunTests(Action):
    name: str = "GenerateAndRunTests"

    async def run(self):
        result = subprocess.run(["python", "-c", "print('Test code command placeholder')"], capture_output=True, text=True).stdout
        logger.info(f"{result=}")
        return result
    
    
class TestAgent(Role):
    name: str = "Test Agent"
    profile: str = "Handles testing pull requests"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([GenerateAndRunTests])
        self._watch([TestPlan])
    
    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        result = await todo.run()

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg