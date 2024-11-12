from metagpt.roles import Role
from metagpt.actions import Action, UserRequirement
from metagpt.team import Message

class BuildPlan(Action):
    name: str = "BuildAndTestPlan"

    PROMPT_TEMPLATE: str = """
    Based on the product requirement, come up with how we can build the code. If no need, just output No Need to Build.
    The code is: {context}
    """

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)

        rsp = await self._aask(prompt)

        return rsp
    
class TestPlan(Action):
    name: str = "TestPlan"

    PROMPT_TEMPLATE: str = """
    Based on the product requirement, come up with a plan to test the following code. Include what kind of tests you would run and the functions/methods that you would test.
    The code is: {context}
    """

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)

        rsp = await self._aask(prompt)

        return rsp

class CodeReviewPlan(Action):
    name: str = "CodeReviewPlan"

    PROMPT_TEMPLATE: str = """
    Based on the product requirement, come up with a plan to review the following code. Include from which aspects you would check the quality of the code.
    The code is: {context}
    """

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)

        rsp = await self._aask(prompt)

        return rsp
    
class CodeDocumentPlan(Action):
    name: str = "CodeDocumentPlan"

    PROMPT_TEMPLATE: str = """
    Based on the product requirement, come up with a plan to document the following code. Include for which classes/functions/methods you would write the documentation. No need to output the actual documentation, only output the plan.
    The code is: {context}
    """

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)

        rsp = await self._aask(prompt)

        return rsp

class RiskAnalysisPlan(Action):
    name: str = "RiskAnalysisPlan"

    PROMPT_TEMPLATE: str = """
    Based on the product requirement, come up with a plan to analyze the risks of the following code. Include what kind of risks you would check for.
    The code is: {context}
    """

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)

        rsp = await self._aask(prompt)

        return rsp

class MainControlAgent(Role):
    name: str = "Main Control Agent"
    profile: str = "Coordinator of the CI/CD pipeline"
    goal: str = "To coordinate a multi-agent LLM-driven automatic CI/CD pipeline"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([BuildPlan, TestPlan, CodeReviewPlan, CodeDocumentPlan, RiskAnalysisPlan])
        self._set_react_mode(react_mode="by_order")
        self._watch([UserRequirement])

    async def _act(self):
        todo = self.rc.todo
        context = self.get_memories()[0]
        result = await todo.run(context=context)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
