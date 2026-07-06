from langchain_ollama import ChatOllama

llm = ChatOllama(
  model="gemma3:12b-it-qat",
  temperature=0,
)

def ask(messages):
  return llm.invoke(messages).content