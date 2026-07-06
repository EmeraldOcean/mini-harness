import re
import json
from llm import ask
from prompts import make_first_prompt, summary_prompt
from registry import get_tool, get_all_tools

tool_infos = get_all_tools()

def clean_json_output(output: str) -> str:
  return re.sub(r"^```json\s*|\s*```$", "", output.strip(), flags=re.DOTALL).strip()

def run(contexts: list):
  prompt = make_first_prompt(contexts, tool_infos)
  result = ask(prompt)
  content = clean_json_output(result)
  parsed = json.loads(content)
  tool_name = parsed.get("tool")
  tool = get_tool(tool_name)

  if tool_name is None or tool is None:
    return ask(contexts)

  args = parsed.get("parameters", {})
  output = tool.run(**args)

  prompt_summary = summary_prompt(contexts, output)
  response = ask(prompt_summary)
  return response
