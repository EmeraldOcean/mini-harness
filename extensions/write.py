from extensions.base import BaseTool
from contexts_result import ToolResult

class WriteTool(BaseTool):
  name = "write"
  description = "파일에 쓰는 도구입니다."
  parameters = {
    "file_path": "쓸 파일 경로",
    "content": "파일에 쓸 내용"
  }

  def run(self, file_path, content):
    try:
      with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
        return ToolResult(
          name=self.name,
          parameters={"file_path": file_path},
          success=True,
          content=content
        )
    except Exception as e:
      return ToolResult(
        name=self.name,
        parameters={"file_path": file_path},
        success=False,
        error=f"파일을 읽는 중 오류가 발생했습니다: {str(e)}"
      )