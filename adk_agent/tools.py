from google.adk.tools import ToolContext
from google.adk.tools.agent_tool import AgentTool
from .sub_agents import ds_agent

async def call_ds_agent(
    question: str,
    tool_context: ToolContext,
):
    """Tool to call data science (nl2py) agent."""

    input_data = tool_context.state["query_result"]

    question_with_data = f"""
  Question to answer: {question}

  Actual data to analyze previous question is already in the following:
  {input_data}

  """

    agent_tool = AgentTool(agent=ds_agent)

    ds_agent_output = await agent_tool.run_async(
        args={"request": question_with_data}, tool_context=tool_context
    )
    tool_context.state["ds_agent_output"] = ds_agent_output
    return ds_agent_output
