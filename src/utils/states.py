import operator
from typing import Annotated, Any, NotRequired, TypedDict

from langgraph.graph import MessagesState, StateGraph
from pydantic import BaseModel, Field

from src.utils.objects import Analyst


class GenerateAnalystsState(TypedDict):
    topic: str  # Research topic
    max_analysts: int  # Number of analysts
    human_analyst_feedback: NotRequired[str | None]  # Human feedback
    analysts: NotRequired[list[Analyst]]  # Analyst asking questions


class InterviewState(MessagesState):
    max_num_turns: int  # Number turns of conversation
    context: Annotated[list, operator.add]  # Source docs
    analyst: Analyst  # Analyst asking questions
    interview: str  # Interview transcript
    sections: list  # Final key we duplicate in outer state for Send() API


class SearchQuery(BaseModel):
    search_query: str = Field(description="Search query for retrieval.")


class ResearchGraphState(TypedDict):
    topic: str  # Research topic
    max_analysts: int  # Number of analysts
    human_analyst_feedback: NotRequired[str | None]  # Human feedback
    analysts: list[Analyst]  # Analyst asking questions
    sections: Annotated[list, operator.add]  # Send() API key
    introduction: str  # Introduction for the final report
    content: str  # Content for the final report
    conclusion: str  # Conclusion for the final report
    final_report: str  # Final report


def state_graph(schema: type[Any]) -> StateGraph:
    """TypedDict is a valid LangGraph schema; pyrefly will not treat it as StateLike."""
    return StateGraph(schema)


def parse_model[T: BaseModel](schema: type[T], value: object) -> T:
    if isinstance(value, schema):
        return value
    if isinstance(value, dict):
        return schema.model_validate(value)
    raise TypeError(f"Expected {schema.__name__}, got {type(value).__name__}")
