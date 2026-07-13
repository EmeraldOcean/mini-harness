import json
import re
from registry import get_tool, get_all_tools
from prompts import make_first_prompt
from llm import ask


def clean_json_output(output: str) -> str:
  return re.sub(r"^```json\s*|\s*```$", "", output.strip(), flags=re.DOTALL).strip()


class Planner:
  tool_infos = get_all_tools()
  
  def plan(self, contexts: list):
    prompt = make_first_prompt(contexts, self.tool_infos)
    result = ask(prompt)
    content = clean_json_output(result)
    parsed = json.loads(content)
    tool_name = parsed.get("tool")
    tool = get_tool(tool_name)

    if tool_name is None or tool is None:
      return None
    
    args = parsed.get("parameters", {})
    return tool, args