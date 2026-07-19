from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langsmith import traceable
import os   


MaxIterations = 10
Model = "qwen3:1.7b"

# --- Tools Decorator --- #

@tool
def get_product_price(product: str) -> float:
    """
    Look for the price of a product from the catalog.
    """
    print(f"Looking for the price of the product: {product}")
    prices = {"Laptop": 999.99, "Smartphone": 699.99, "Keyboard": 199.99}
    return prices.get(product, 0)


@tool
def apply_discount(price: float, discount: str) -> float:
    """
    Apply a discount tier to the price of a product and return the discounted price.
    Available discount tiers: Gold, Silver, Bronze    
    """
    print(f" >> Applying discount for {price} with discount tier {discount}")
    discount_tiers = {"Gold": 10, "Silver": 5, "Bronze": 2}
    discount = discount_tiers.get(discount, 0)
    return round(price * (1 - discount / 100), 2)

# -- Agent Loop -- #

@traceable(name="Langchain Agent Loop")
def run_agent(question: str):
    tools = (get_product_price, apply_discount)
    tool_dict = {t.name: t for t in tools}

    llm = init_chat_model(f"ollama:qwen3:1.7b", temperature=0)
    llm_with_tools = llm.bind_tools(tools)  

    print(f"Question: {question}")
    print("=" * 50)

    messages = [

        SystemMessage(

            content=(
                "You are a helpful Shopping Assistant"
                "You have access to product catalog and discount tiers."
                "Strict Rules - You should follow this exactly:\n"
                "1. Never guess or assume product price.\n"
                "You must call get_product_price tools to get the price of a product.\n"
                "2. Only call apply_discount after you have the price of a product.\n"
                "Use the exact price returned by get_product_price to call apply_discount.\n"
                "3. Never calculate the discounted price yourself."
                "Always use the apply_discount tool to apply discount price"
                "4. If user doesnt specify discount tier, you should ask user to specify discount tier before applying discount."
            )
        ),
        HumanMessage(content=question)

    ]

    for iteration in range(MaxIterations + 1):
        print(f"--Iteration {iteration} --")

        ai_message = llm_with_tools.invoke(messages)

        tool_calls = ai_message.tool_calls

        if not tool_calls:
            print("No tool calls made. Final Answer:")
            print(ai_message.content)
            break

        tool_call = tool_calls[0]
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args")
        tool_call_id = tool_call.get("id")
        print(f"Tool Call: {tool_name} with input: {tool_args}")

        tool_to_use = tool_dict.get(tool_name)
        if not tool_to_use:
            print(f"Tool {tool_name} not found. Skipping tool call.")
            continue
        observation = tool_to_use.invoke(tool_args)

        print(f"Observation: {observation}")

        messages.append(ai_message)
        messages.append(ToolMessage(content=observation, tool_call_id=tool_call_id))

if __name__ == "__main__":
    print("Hello! Langchain Agent")
    result = run_agent("What is the price of a Laptop after discount with Gold Membership?")