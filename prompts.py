from contexts_result import ToolResult


def _get_last_user(contexts: list):
  for c in reversed(contexts):  # c type : Message
    if c.role == "user":
      user_input = c.content
      break
  return user_input


def _get_first_user(contexts: list):
  for c in contexts:  # c type : Message
    if c.role == "user":
      user_input = c.content
      break
  return user_input


def _make_context_prompt(contexts: list) -> str:
  context_str = ""
  for c in contexts:
    if c.role == "user":
      context_str += f"""
                      [User]
                      Content: {c.content}
                      """
    elif c.role == "assistant":
      context_str += f"""
                      [Assistant]
                      Content: {c.content}
                      """
    elif c.role == "tool":
      result = c.content  # c.content type : ToolResult
      if isinstance(result, ToolResult):
        context_str +=f"""
                        [Tool Result]
                        Tool Name: {result.name}
                        Arguments: {result.parameters}
                        Status: {"SUCCESS" if result.success else "FAILED"}
                        Output: {result.content}
                        Error: {result.error}
                        [End Tool Result]
                       """
  return context_str


def make_first_prompt(contexts: list, all_tools) -> str:
  tool_descriptions = []

  for idx, tool in enumerate(all_tools):
    tool_descriptions.append(f"""{idx+1}. name: {tool.name}
                             description: {tool.description}
                             parameters: {tool.parameters}"""
                             )

  tool_prompt = "\n".join(tool_descriptions)
  result =  f"""
  # Goal
  사용자의 최종 목표
  {_get_first_user(contexts)}
  
  # Current State
  지금까지의 대화와 Tool 실행 기록
  {_make_context_prompt(contexts)}

  # Available Tools
  {tool_prompt}

  # Instructions
  1. 현재 목표가 이미 완료되었는지 먼저 판단한다.
  2. Current State에는 이전 대화와 Tool 실행 결과가 포함되어 있다.
  Tool Result의 output은 실제 Tool 실행 결과 데이터이다.
  3. Tool Result를 확인하여:
   - 이미 필요한 정보를 확보했다면 같은 Tool을 다시 호출하지 않는다.
   - 확보한 정보를 이용해 다음 단계가 필요하면 다음 Tool을 호출한다.
  4. 현재 목표가 완료되어 더 이상 Tool이 필요하지 않다면
    - 형식:
      {{
      "tool": null,
      "parameters": {{}}
    }}
    를 반환한다.
  5. 완료되지 않았다면 목표 달성을 위한 가장 적합한 다음 Tool 하나만 선택한다.
  - 형식:
  {{
    "tool": "도구 이름",
    "parameters": {{
      "파라미터명": "값"
    }}
  }}
  6. 반드시 JSON만 출력한다.
  """
  return result


def summary_prompt(contexts: list) -> str:
  user_input = _get_last_user(contexts)
  return f"""
  # 현재 사용자가 입력한 질문
  user_input : {user_input}

  # 지금까지 진행된 대화의 맥락
  contexts : {_make_context_prompt(contexts)}

  # Instructions
  지금까지의 작업을 바탕으로, 사용자가 원하는 최종 결과를 이해하기 쉽게 자연스러운 문장으로 바꿔 채팅으로 답변한다.
  """