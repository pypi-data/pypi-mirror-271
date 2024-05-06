from langchain.agents import AgentExecutor
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool

class SecondPersona(BaseModel):
    """
    Generic Agent
    """
    agent: AgentExecutor
    name: str
    scope: str
    instructions : str

    def as_tool(self):

        class Input(BaseModel):
            task: str = Field(description=self.instructions)

        def get_response(task: str):
            response = self.agent.invoke({"input":task})
            return response

        tool = StructuredTool.from_function(
            func=get_response,
            name=self.name,
            description=self.scope,
            args_schema=Input,
            # coroutine= ... <- you can specify an async method if desired as well
        )

        return tool
