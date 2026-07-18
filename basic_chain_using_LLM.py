from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

import os
load_dotenv()

def chainagent():
    info = """
    Elon Reeve Musk (/ilɒn/ ⓘ EE-lon; born June 28, 1971) is a businessman and former public official who is the CEO and largest shareholder of Tesla and SpaceX. Musk has been the wealthiest person in the world since 2025, and became the only trillionaire in terms of US dollars in June 2026; as of July 10, 2026, Forbes estimates his net worth to be US$917 billion.  """

    summary_template = """
    You are a summarization engine, use this {info}. You will be given a text and you will summarize it in 2 sentences."""

    summary_prompt_template = PromptTemplate(input_variables=["info"], template=summary_template)

    LLM = ChatOllama(model="gemma3:270m", temperature=0.7)

    chain = summary_prompt_template | LLM  
    
    response = chain.invoke(input={"info": info})
    return response.content

responsecontent = chainagent()
print(responsecontent)
