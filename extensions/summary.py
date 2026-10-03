from extensions.base import BaseTool
from contexts import ToolResult
from llm import ask

class SummaryTool(BaseTool):
  name = "summary"
  description = "파일 내용을 요약하는 도구입니다."
  observation = """
  내용 요약 완료.
  현재 상태에 요약된 내용이 저장되어 있다.
  추가 작업(번역, 저장 등)이 필요하다면 확보한 내용을 활용한다.
  """
  artifact_type = "summary"
  inputs = {
    "content": "document"
  }
  retryable = False
  
  def run(self, content):
    result = ask(f"""
      다음 내용을 요약하라.
                   
      {content}
      """
    )
    return ToolResult(
      name=self.name,
      parameters=self.parameters,
      success=True,
      content=result,
      observation=self.observation,
      artifact_type=self.artifact_type
    )
    
  def prepare_args(self, args, contexts_manager):
    if "content" not in args:
      args["content"] = contexts_manager.get_artifact("document")
    return args