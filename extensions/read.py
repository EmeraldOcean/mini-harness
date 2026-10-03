from extensions.base import BaseTool
from contexts import ToolResult

class ReadTool(BaseTool):
  name = "read"
  description = "파일을 읽는 도구입니다."
  parameters = {
    "file_path": "읽을 파일 경로"
  }
  observation = """
  파일 내용 확보 완료.
  현재 상태에 파일 내용이 저장되어 있다.
  추가 작업(요약, 번역, 저장 등)이 필요하다면 확보한 내용을 활용한다.
  """
  artifact_type = "document"
  retryable = False

  def run(self, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
      result = file.read()
    return ToolResult(
      name=self.name,
      parameters=self.parameters,
      success=True,
      content=result,
      observation=self.observation,
      artifact_type=self.artifact_type
    )