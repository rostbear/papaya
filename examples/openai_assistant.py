import sys
import os
import math
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from papaya import Agent, tool
from papaya.models.openai import OpenAIModel

load_dotenv()


@tool
def calculate_square_root(number: float) -> float:
    """Calculate the square root of a number."""
    return math.sqrt(float(number))


def main():
    model = OpenAIModel(model_name="gpt-4o-mini")
    
    agent = Agent(
        model=model,
        instructions="Sei un utile assistente matematico.",
        tools=[calculate_square_root],
        max_steps=5,
    )

    question = "Qual è la radice quadrata di 255025?"
    print(f"Utente: {question}")
    print("Elaborazione in corso con OpenAI...\n")
    
    result = agent.run(question)
    
    print("--- Risposta ---")
    print(result.text)


if __name__ == "__main__":
    main()
