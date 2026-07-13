from extensions.base import BaseTool
from contexts import ToolResult

class WriteTool(BaseTool):
  name = "write"
  description = "파일에 쓰는 도구입니다."
  parameters = {
    "file_path": "쓸 파일 경로",
    "content": "파일에 쓸 내용"
  }
  observation = """
  파일 내용 작성 완료.
  사용자가 요청한 저장 작업이 수행되었다.
  동일한 내용을 다시 저장할 필요가 없다.
  """

  def run(self, file_path, content):
    try:
      with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
      return ToolResult(
        name=self.name,
        parameters={"file_path": file_path},
        success=True,
        content="파일에 성공적으로 작성되었습니다.",
        observation=self.observation
      )
    except Exception as e:
      return ToolResult(
        name=self.name,
        parameters={"file_path": file_path},
        success=False,
        error=f"파일을 쓰는 중 오류가 발생했습니다: {str(e)}"
      )