import subprocess
import re

from metagpt.actions import Action
from metagpt.logs import logger


def parse_code(rsp, lang="python"):
    pattern = r"```" + lang + r"(.*)```"
    match = re.search(pattern, rsp, re.DOTALL)
    code_text = match.group(1) if match else rsp
    return code_text


class BuildPlan(Action):
    name: str = "BuildPlan"

    PROMPT_TEMPLATE: str = """
    Based on the product requirement, come up with the command to build the provided code proect.
    Return ```bash your_command_here``` with NO other texts
    If you believe no building command is needed, your command should be 'pass'
    The provided code project is: {context}
    """

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)

        rsp = await self._aask(prompt)

        rsp = parse_code(rsp, lang="bash")

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


class BuildCode(Action):
    name: str = "BuildCode"
    
    async def run(self, context, hard_coded_build_command = ""):

        if 'pass' in context:
            result = "According to the coordinater, no building command is needed."
        else:
            if hard_coded_build_command:
                context = hard_coded_build_command
            result = subprocess.run([context], capture_output=True, text=True).stdout
        logger.info(f"{result=}")
        return result


class GenerateAndRunTests(Action):
    name: str = "GenerateAndRunTests"

    async def run(self):
        result = subprocess.run(["python", "-c", "print('Test code command placeholder')"], capture_output=True, text=True).stdout
        logger.info(f"{result=}")
        return result

    
class AnalyzeBuildTestResults(Action):
    name: str = "AnalyzeBuildTestResults"

    PROMPT_TEMPLATE: str = """
    Analyzing build and test results: {output}
    """

    async def run(self, build_test_output: str):
        prompt = self.PROMPT_TEMPLATE.format(output=build_test_output)

        rsp = await self._aask(prompt)

        return rsp