import json
import re
from registry import get_tool, get_all_tools
from prompts import make_first_prompt
from llm import ask


def clean_json_output(output: str) -> str:
  return re.sub(r"^```json\s*|\s*```$", "", output.strip(), flags=re.DOTALL).strip()


class Planner:
  def __init__(self):
    self.tool_infos = get_all_tools()
    self.tool_history = []
  
  def plan(self, contexts: list):
    try:
      prompt = make_first_prompt(contexts, self.tool_infos)
      result = ask(prompt)
      content = clean_json_output(result)
      parsed = json.loads(content)
      tool_name = parsed.get("tool")
      tool = get_tool(tool_name)

      if tool_name is None or tool is None:
        return None
      
      args = parsed.get("parameters", {})

      if self._is_duplicate(tool, args):
        return None

      return tool, args
    except json.JSONDecodeError as e:
      print(f"JSON 파싱 오류: {str(e)}")
      return None

    except Exception as e:
      print(f"계획 수립 중 오류 발생: {str(e)}")
      return None


  def record_execution(self, tool, args):
    self.tool_history.append({
      "name": tool.name,
      "parameters": args
    })

  def _is_duplicate(self, tool, args):
    for record in self.tool_history:
      if (record["name"] == tool.name) and (record["parameters"] == args):
        return True
    return False