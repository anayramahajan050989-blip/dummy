import os
os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

from langchain_mcp_adapters.client import MultiServerMCPClient

mcp_client = MultiServerMCPClient(
    {
        "gcp": {
            "command": "python",
            "args": ["gcp_mcp_server.py"],
            "transport": "stdio",
        }
    }
)

tools = await mcp_client.get_tools()

from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain import hub

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = hub.pull("hwchase17/openai-tools-agent")

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

await agent_executor.ainvoke(
    {"input": "List all GCS buckets in my project"}
)