REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use this format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question formatted according to format_instructions: {format_instructions}

IMPORTANT:
- Only use "Final Answer:" when you have enough information to answer completely
- The Final Answer must be valid JSON with "answer" and "sources" fields
- After getting search results, analyze them and provide the final JSON answer
- Do NOT output raw JSON anywhere except after "Final Answer:"

Question: {input}
Thought:{agent_scratchpad}
"""
