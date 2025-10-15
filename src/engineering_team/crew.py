from __future__ import annotations

import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class EngineeringTeam:
    """EngineeringTeam crew wired to config/agents.yaml and config/tasks.yaml"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # ---------- Agents ----------
    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config["engineering_lead"],
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["backend_engineer"],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Docker sandbox (if enabled)
            max_execution_time=600,
            max_retry_limit=3,
        )

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["frontend_engineer"],
            verbose=True,
        )

    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["test_engineer"],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=600,
            max_retry_limit=3,
        )

    # ---------- Tasks ----------
    @task
    def design_task(self) -> Task:
        # Produces: output/{module_name}_design.md
        return Task(config=self.tasks_config["design_task"])

    @task
    def code_task(self) -> Task:
        # Consumes design_task via YAML 'context'
        # Produces: output/{module_name}
        return Task(config=self.tasks_config["code_task"])

    @task
    def frontend_html_task(self) -> Task:
        # Produces: output/web/index.html
        return Task(config=self.tasks_config["frontend_html_task"])

    @task
    def frontend_css_task(self) -> Task:
        # Produces: output/web/styles.css
        return Task(config=self.tasks_config["frontend_css_task"])

    @task
    def frontend_js_task(self) -> Task:
        # Produces: output/web/app.js
        return Task(config=self.tasks_config["frontend_js_task"])

    @task
    def test_task(self) -> Task:
        # Consumes code_task via YAML 'context'
        # Produces: output/test_{module_name}
        return Task(config=self.tasks_config["test_task"])

    # ---------- Crew ----------
    @crew
    def crew(self) -> Crew:
        """Creates the engineering crew with sequential execution."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
