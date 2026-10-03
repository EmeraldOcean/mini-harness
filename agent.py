from llm import ask
from prompts import summary_prompt
from planner import Planner
from contexts import Message, ContextManager

context_manager = ContextManager()
planner = Planner()
MAX_RETRY = 3  # 최대 재시도 횟수
retry_count = 0  # 현재 재시도 횟수

def run(user_input: str) -> str:
  context_manager.add(Message(
    role="user",
    content=user_input
  ))

  while True:
    action = planner.plan(context_manager.get_messages())  # 다음 계획 결정
    print("Planner >>", action)

    if action is None:
      final_prompt = summary_prompt(context_manager.get_messages())
      response = ask(final_prompt)
      context_manager.add(Message(
        role="assistant",
        content=response
      ))
      return response

    else:
      tool, args = action
      retry_count = 0

      while retry_count < MAX_RETRY:
        args = tool.prepare_args(args, context_manager)
        output = tool.run(**args)

        if output.success:
          break
        retry_count += 1

        print(f"Tool execution failed. Retry {retry_count}/{MAX_RETRY}. Error: {output.error}")

        if not tool.retryable:
          break

      context_manager.add(Message(
        role="tool",
        content=output
      ))