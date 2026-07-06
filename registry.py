from extensions import ReadTool, WriteTool

tools = {
  ReadTool().name: ReadTool(),
  WriteTool().name: WriteTool(),
}

def register(name, func):
  tools[name] = func

def get_tool(name):
  return tools.get(name)

def get_all_tools():
  return tools.values()