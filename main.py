from dotenv import load_dotenv

from src.vector_store import load_vector_store
from src.assistant import AIResearchAssistant
from src.agent import build_research_agent


def main():
    load_dotenv()

    vector_store = load_vector_store()

    assistant = AIResearchAssistant(vector_store)
    agent = build_research_agent(assistant)

    print("\nAI Research Agent")
    print("Type naturally.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        result = agent.invoke({
            "user_input": user_input
        })

        print("\nAgent:")
        print(result["answer"])
        print()


if __name__ == "__main__":
    main()