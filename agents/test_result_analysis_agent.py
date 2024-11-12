from metagpt.roles import Role
from metagpt.actions import Action
from metagpt.logs import logger
from metagpt.team import Message
import subprocess
from CS410FP.agents.build_agent import BuildCode, RunTests
    



class TestResultAnalysisAgent(Role):
    name: str = "Build and Test Agent"
    profile: str = "Handles building and testing pull requests"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([AnalyzeBuildTestResults])
        self._watch()

    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        msg = self.get_memories(k=1)[0]
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
