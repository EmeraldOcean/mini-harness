def parse_contexts(contexts: list):
  user_input = contexts[-1]["content"]
  prev_contexts = contexts[:-1]
  prev_contexts_str = "\n".join([f"{c['role']}: {c['content']}" for c in prev_contexts])
  return user_input, prev_contexts_str
  

def make_first_prompt(contexts: list, all_tools) -> str:
  user_input, prev_contexts_str = parse_contexts(contexts)
  tool_descriptions = []

  for idx, tool in enumerate(all_tools):
    tool_descriptions.append(f"""{idx+1}. name: {tool.name}
                             description: {tool.description}
                             parameters: {tool.parameters}"""
                             )

  tool_prompt = "\n".join(tool_descriptions)
  result =  f"""
  당신은 도구 호출 시스템과 일반 채팅을 동시에 처리할 수 있는 AI입니다.
  아래는 이전 대화의 맥락입니다.
  {prev_contexts_str}
  아래는 현재 사용자의 질문입니다.
  {user_input}
  사용자 질문을 보고, 만약 도구 호출이 필요하면 JSON 형식으로 출력하세요.
  
  도구 목록:
  {tool_prompt}

  규칙:
  1. 도구가 반드시 필요한 경우에만 Tool을 호출한다.
  - 형식:
  {{
    "tool": "도구 이름",
    "parameters": {{
      "파라미터명": "값"
    }}
  }}
  2. 일반적인 대화는 절대 Tool을 호출하지 않는다.
  3. Tool이 필요 없다면 다음 JSON을 출력한다.
  - 형식:
    {{
    "tool": null,
    "parameters": {{}}
  }}
  4. 이미 실행된 Tool과 그 결과는 이전 대화 맥락에 포함되어 있으므로, 같은 Tool을 반복해서 호출하지 않는다.

  사용자 질문: "{user_input}"
  """
  return result


def summary_prompt(contexts: list, tool_output: str) -> str:
  user_input, _ = parse_contexts(contexts)
  return f"""
  {user_input}
  위는 사용자가 입력했던 질문이고, 아래는 도구 실행 결과입니다.
  만약 도구 실행 결과가 None이라면 아래 명령은 무시하세요.
  도구 실행 결과가 None이 아니라면, 해당 결과를 사용자가 이해하기 쉽게 자연스러운 문장으로 바꿔 채팅으로 답변해 주세요:
  {tool_output}
  """