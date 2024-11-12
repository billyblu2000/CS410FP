import asyncio

from metagpt.team import Team

from agents.main_control_agent import MainControlAgent
from agents.build_agent import BuildAgent
from agents.test_agent import TestAgent
# from agents.test_result_analysis_agent import TestResultAnalysisAgent
# from agents.code_review_agent import CodeReviewAgent
# from agents.code_document_agent import CodeDocumentAgent
# from agents.risk_analysis_agent import RiskAnalysisAgent

async def main(initial_prompt):
    cicd_team = Team()
    cicd_team.hire([
        MainControlAgent(),
        BuildAgent(),
        TestAgent(),
        # TestResultAnalysisAgent(),
        # CodeReviewAgent(),
        # CodeDocumentAgent(),
        # RiskAnalysisAgent(),
    ])

    cicd_team.invest(investment=0.1)
    cicd_team.run_project(initial_prompt)

    await cicd_team.run(n_round=2)

if __name__ == "__main__":

    project = 'example_project.py'

    with open(project, 'r') as file:
        initial_prompt = file.read()

    asyncio.run(main(initial_prompt))