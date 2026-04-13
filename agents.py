from langchain.agents import initialize_agent
from langchain_community.llms import Ollama
from tools import calculator, weather
from memory import research_memory, summary_memory

llm = Ollama(model="gemma:2b")

# Research Agent
research_agent = initialize_agent(
tools=[calculator, weather],
llm=llm,
memory=research_memory,
agent="zero-shot-react-description",
verbose=True,
handle_parsing_errors=True,
max_iterations=5,
early_stopping_method="generate"
)

# Summarizer Agent
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="Give only the final answer in one short sentence: {text}"
)
summarizer_agent = LLMChain(
    llm=llm,
    prompt=summary_prompt
)