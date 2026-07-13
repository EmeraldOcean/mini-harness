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

  def run(self, file_path):
    try:
      with open(file_path, 'r', encoding='utf-8') as file:
        result = file.read()
      return ToolResult(
        name=self.name,
        parameters={"file_path": file_path},
        success=True,
        content=result,
        observation=self.observation
      )
    except Exception as e:
      return ToolResult(
        name=self.name,
        parameters={"file_path": file_path},
        success=False,
        error=f"파일을 읽는 중 오류가 발생했습니다: {str(e)}"
      )