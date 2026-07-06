from extensions.base import BaseTool

class ReadTool(BaseTool):
  name = "read"
  description = "파일을 읽는 도구입니다."
  parameters = {
    "file_path": "읽을 파일 경로"
  }

  def run(self, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
      result = file.read()
    return result