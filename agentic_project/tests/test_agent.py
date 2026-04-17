import pytest
from agents.main_agent import Agent

def test_agent_run():
    agent = Agent()
    response = agent.run("What is 2 + 2?")
    assert "4" in response

def test_agent_calculate_tool():
    agent = Agent()
    tools = agent._get_tools()
    calculate_tool = next((tool for tool in tools if tool.name == "calculate"), None)
    assert calculate_tool is not None
    result = calculate_tool.run({"expression": "2 * 3"})
    assert "6" in result