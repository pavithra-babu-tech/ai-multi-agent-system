from agents import research_agent, summarizer_agent
from memory import shared_memory
import re

def multi_agent_system(user_query):

    # SUMMARIZE CASE
    if "summarize" in user_query.lower():
        past_data = shared_memory.load_memory_variables({"input": user_query})
        history = past_data.get("history", "")

        # Extract last AI answer
        if "AI:" in history:
            research_output = history.split("AI:")[-1].strip()
        else:
            research_output = history

    # NORMAL CASE
    else:
        if any(op in user_query for op in ["+", "-", "*", "/"]):
            try:
                expression = re.findall(r'[0-9+\-*/.]+', user_query)
                expression = "".join(expression)
                research_output = str(eval(expression))
            except:
                research_output = "calculation error"
        else:
            research_output = research_agent.run(user_query)

        # Save to memory
        shared_memory.save_context(
            {"input": user_query},
            {"output": research_output}
        )

    # FINAL OUTPUT
    if "summarize" in user_query.lower():
        final_output = summarizer_agent.invoke({"text": research_output})["text"]
    else:
        final_output = research_output

    return final_output


if __name__ == "__main__":
    print("Multi-Agent System Started (type 'exit' to quit)")

    while True:
        query = input("You: ")

        if not query.strip():
            continue

        if query.lower() == "exit":
            break

        response = multi_agent_system(query)
        print("AI:", response)
        
def full_workflow(user_query):

    # Step 1: Research
    research_output = multi_agent_system(user_query)

    # Step 2: Summarize
    summary = summarizer_agent.invoke({"text": research_output})["text"]

    # Step 3: Compose Email
    email = f"""
Subject: Information about {user_query}

Dear Sir/Madam,

Here is the information:

{summary}

Thank you.
"""

    return {
        "research": research_output,
        "summary": summary,
        "email": email
    }
