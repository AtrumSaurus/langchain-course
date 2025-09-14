from dotenv import load_dotenv

load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse

tools = [TavilySearch()]
llm = ChatOpenAI(model="gpt-4o")
react_prompt = hub.pull("hwchase17/react")

output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tool_names"],
).partial(format_instructions=output_parser.get_format_instructions())

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt_with_format_instructions,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    # max_iterations=5,  # Limit iterations to prevent infinite loops
    # handle_parsing_errors=True,  # Handle parsing errors gracefully
    # return_intermediate_steps=True,
)


def safe_parse_output(text):
    """Safely parse the output with fallback handling"""
    try:
        return output_parser.parse(text)
    except Exception as e:
        print(f"Parse error: {e}")
        # Try to extract JSON from the text if direct parsing fails
        import re

        json_pattern = r'\{[^}]*"answer"[^}]*\}'
        matches = re.findall(json_pattern, text, re.DOTALL)
        if matches:
            try:
                import json

                parsed = json.loads(matches[0])
                return AgentResponse(**parsed)
            except:
                pass

        # Fallback: create a basic response
        return AgentResponse(answer=text, sources=[])


extract_output = RunnableLambda(lambda x: x["output"])
parse_output = RunnableLambda(lambda x: output_parser.parse(x))
# parse_output = RunnableLambda(safe_parse_output)

chain = agent_executor | extract_output | parse_output


def main():
    result = chain.invoke(
        input={
            "input": "search for 3 jobs for an ai engineer in the SF bay area on linkedin and list their details"
        }
    )
    print(result)


if __name__ == "__main__":
    try:
        main()
    finally:
        import gc

        gc.collect()
