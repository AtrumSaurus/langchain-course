from typing import List

from pydantic import BaseModel, Field


class Source(BaseModel):
    """Schema for source used by the Agent"""

    url: str = Field(description="URL of the source")


class AgentResponse(BaseModel):
    """Schema for agent response wint answer and sources"""

    answer: str = Field(description="The agent's answer to the query")
    sources: List[Source] = Field(
        default_factory=list, description="List of sources to generate the answer"
    )
