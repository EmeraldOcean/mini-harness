from contexts import ToolResult


def _get_last_user(contexts: list) -> str:
  for c in reversed(contexts):  # c type : Message
    if c.role == "user":
      user_input = c.content
      break
  return user_input


def _get_first_user(contexts: list) -> str:
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
                        Observation: {result.observation}
                        Artifact Type: {result.artifact_type}
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
  1. 사용자의 전체 목표를 기준으로 판단한다.
  2. 현재 단계가 목표의 일부만 완료된 상태라면 다음 Tool을 선택한다.
  3. 최종 결과물이 필요한 경우 반드시 마지막 출력 저장/전달 단계까지 수행한다.
  4. Current State에는 이전 대화와 Tool 실행 결과가 포함되어 있다.
    - Tool Result의 output은 실제 Tool 실행 결과 데이터이다.
  5. Tool 실행이 실패한 경우:
    - error 내용을 확인한다.
    - retryable이면 동일 Tool 재시도를 고려한다.
    - retry 불가능하면 다른 해결 방법을 찾거나 사용자에게 요청한다.
  6. 실패한 Tool 결과를 성공한 것으로 간주하지 않는다.
  7. 현재 목표가 완료되어 더 이상 Tool이 필요하지 않다면
    - 형식:
      {{
      "tool": null,
      "parameters": {{}}
    }}
    를 반환한다.
  8. 완료되지 않았다면 목표 달성을 위한 가장 적합한 다음 Tool 하나만 선택한다.
  - 형식:
  {{
    "tool": "도구 이름",
    "parameters": {{
      "파라미터명": "값"
    }}
  }}
  9. 반드시 JSON만 출력한다.
   - 문자열 내부 줄바꿈은 반드시 \\n으로 escape하고, 임의의 \\를 넣지 않는다.
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