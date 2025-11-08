from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from langchain_ollama import OllamaLLM


@CrewBase
class FinancialResearcher():
    """FinancialResearcher crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        # Initialize Ollama LLM
        try:
            self.llm = OllamaLLM(
                model="ollama/llama2",
                temperature=0.7,
                base_url="http://localhost:11434"
            )
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            raise

    @agent
    def researcher(self) -> Agent:
        from financial_researcher.tools.custom_tool import GoldMarketResearchTool
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            llm=self.llm,
            tools=[GoldMarketResearchTool()],
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'], # type: ignore[index]
            llm=self.llm,
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'], # type: ignore[index]
            llm=self.llm,
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )
    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
        )
    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'], # type: ignore[index]
            output_file='financial_report.md'
        )
    
    @crew
    def financial_researcher_crew(self) -> Crew:    
        return Crew(
            agents=[
                self.researcher(),
                self.reporting_analyst(),
                self.writer()
            ],
            tasks=[
                self.research_task(),
                self.reporting_task(),
                self.writing_task()
            ],
            process=Process.sequential,
            verbose=True
        )