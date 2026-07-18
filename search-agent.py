import os
from unittest import result
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool    
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from langchain_tavily import TavilySearch



load_dotenv()



llm = ChatOpenAI(model="gpt-5", temperature=0.9)
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools)

def main():
    result = agent.invoke(
        {
            "messages":[
                HumanMessage(content="Get me Top 3 AI Architect oppurtunities from LinkedIn?")
            ]
         
        }
        )
    print(result)

output = main()






