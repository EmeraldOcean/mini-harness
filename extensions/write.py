from extensions.base import BaseTool
from contexts import ToolResult

class WriteTool(BaseTool):
  name = "write"
  description = """
                파일에 데이터를 저장하는 도구입니다.
                이전 Tool의 결과물을 파일로 저장할 때 사용합니다.
                사용자가 저장을 요청했고 저장할 내용이 존재할 경우 선택합니다.
                """
  parameters = {
    "file_path": "쓸 파일 경로"
  }
  observation = """
  파일 내용 작성 완료.
  사용자가 요청한 저장 작업이 수행되었다.
  동일한 내용을 다시 저장할 필요가 없다.
  """
  inputs = {
    "content": "summary"
  }
  artifact_type = "document"
  retryable = False

  def run(self, file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
      file.write(content)
    return ToolResult(
      name=self.name,
      parameters=self.parameters,
      success=True,
      content="파일에 성공적으로 작성되었습니다.",
      observation=self.observation,
      artifact_type=self.artifact_type
    )

  def prepare_args(self, args, contexts_manager):
    if "content" not in args:
      args["content"] = contexts_manager.get_artifact("summary")
    return args