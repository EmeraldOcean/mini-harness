from extensions.base import BaseTool
from contexts_result import ToolResult

class ReadTool(BaseTool):
  name = "read"
  description = "파일을 읽는 도구입니다."
  parameters = {
    "file_path": "읽을 파일 경로"
  }

  def run(self, file_path):
    try:
      with open(file_path, 'r', encoding='utf-8') as file:
        result = file.read()
      return ToolResult(
        name=self.name,
        parameters={"file_path": file_path},
        success=True,
        content=result
      )
    except Exception as e:
      return ToolResult(
        name=self.name,
        parameters={"file_path": file_path},
        success=False,
        error=f"파일을 읽는 중 오류가 발생했습니다: {str(e)}"
      )