from extensions.base import BaseTool

class WriteTool(BaseTool):
  name = "write"
  description = "파일에 쓰는 도구입니다."
  parameters = {
    "file_path": "쓸 파일 경로",
    "content": "파일에 쓸 내용"
  }

  def run(self, file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
      file.write(content)
    return f"파일 '{file_path}'에 내용이 성공적으로 작성되었습니다."