from llm import ask
from prompts import summary_prompt
from planner import Planner
from contexts import Message

contexts = []
planner = Planner()

def run(user_input: str) -> str:
  contexts.append(Message(
    role="user",
    content=user_input
  ))

  while True:
    action = planner.plan(contexts)  # 다음 계획 결정
    print("Planner >>", action)

    if action is None:
      final_prompt = summary_prompt(contexts)
      response = ask(final_prompt)
      contexts.append(Message(
        role="assistant",
        content=response
      ))
      return response

    else:
      tool, args = action
      output = tool.run(**args)

      contexts.append(Message(
        role="tool",
        content=output
      ))

      planner.record_execution(tool, args)