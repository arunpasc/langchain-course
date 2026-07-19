import os
from unittest import result
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool    
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field



load_dotenv()

class Source(BaseModel):
    url: str = Field(description="The URL of the source")

class AgentResponse(BaseModel):
    answer: str = Field(description="The answer to the user's question")
    sources: list[Source] = Field(description="A list of sources used to generate the answer")



llm = ChatOpenAI(model="gpt-5", temperature=0.9)
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)

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






