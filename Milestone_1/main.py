import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain


def load_environment():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in .env file.")

    return api_key


def initialize_llm():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    return llm


def create_chain(llm):
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant.\n"
        "Answer the following question clearly:\n"
        "{question}"
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt
    )

    return chain


def run_agent(chain):
    print("\n🤖 LangChain Agent Started (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting... Goodbye!")
            break

        if not user_input:
            print("⚠️ Please enter a question.")
            continue

        try:
            response = chain.run(question=user_input)
            print("Agent:", response)

        except Exception as e:
            print("❌ Error:", str(e))


def main():
    try:
        load_environment()
        llm = initialize_llm()
        chain = create_chain(llm)
        run_agent(chain)

    except Exception as e:
        print("❌ Startup Error:", str(e))


if _name_ == "_main_":
    main()
