from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


def main():
    information = """Tendulkar"""

    prompt_template = """You are a cricket expert. Answer about {information} in just 2 lines."""

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=prompt_template,
    )

    LLM = ChatOpenAI(model="gpt-5", temperature=0.9, max_tokens=1000)
    chain = summary_prompt_template | LLM
    result = chain.invoke({"information": information})
    return(result.content)

if __name__ == "__main__":
    response = main()
    print(response)
