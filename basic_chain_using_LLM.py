

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from langchain_ollama import ChatOllama


import os
load_dotenv()


def response():
    information = """
    OpenAI is an American artificial intelligence (AI) research and deployment organization. It is best known for creating ChatGPT—the conversational chatbot that helped launch the global generative AI boom. Founded in 2015, its core mission is to develop safe and beneficial Artificial General Intelligence (AGI) that benefits all of humanity"""

    summary_template = """You are a analyzer, user this information {information}, pick just 2 import points and mention. Do not use more than 25 words"""

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template
    )

  #  LLM = ChatOpenAI(model_name="gpt-5", temperature=0.7)
    LLM = ChatOllama(model="gemma3:270m", temperature=0.7, base_url="http://localhost:11434")  # Use the Ollama model
    chain = summary_prompt_template | LLM
    response = chain.invoke(input={"information": information})
    return response.content

response = response()
print(response)