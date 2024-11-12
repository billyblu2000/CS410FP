from metagpt.roles import Role
from metagpt.actions import  UserRequirement
from metagpt.team import Message

from agents.actions import BuildPlan, TestPlan, CodeReviewPlan, CodeDocumentPlan, RiskAnalysisPlan
from agents.actions import BuildCode


class MainControlAgent(Role):
    name: str = "Main Control Agent"
    profile: str = "Coordinator of the CI/CD pipeline"
    goal: str = """To coordinate a multi-agent LLM-driven automatic CI/CD pipeline. 
    Based on the provided user requirement and project code, you will plan the following stages in order: 
    build, tests, review, generate document, and analyze risk.
    You will complete these stages in order. If you didn't see any previous planning outputs, move on to the first stage (build). Move to the next stage if you see the output previous stages. If all stages are completed, you will stop the process.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([BuildPlan, TestPlan, CodeReviewPlan, CodeDocumentPlan, RiskAnalysisPlan])
        # self._set_react_mode(react_mode="by_order")
        self._watch([UserRequirement, BuildCode])

    async def _act(self):
        todo = self.rc.todo
        context = self.get_memories()
        result = await todo.run(context=context)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
