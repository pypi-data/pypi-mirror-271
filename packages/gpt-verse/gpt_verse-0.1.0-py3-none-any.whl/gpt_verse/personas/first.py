from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from typing import List

class FirstPersona(BaseModel):
    """myAgent"""
    llm: BaseChatModel
    tools: List[BaseTool]
    prompt: str

    def as_executor(self):

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""{self.prompt}""",
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, handle_parsing_errors=True, verbose=True)
        return agent_executor