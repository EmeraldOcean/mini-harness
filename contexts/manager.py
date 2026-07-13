from contexts.tool_result import ToolResult

class ContextManager:
  def __init__(self):
    self.messages = []

  def add(self, message):
    self.messages.append(message)

  def get_messages(self):
    return self.messages

  def get_previous_output(self):
    for message in reversed(self.messages):
      if message.role == "tool":
        result = message.content

        if isinstance(result, ToolResult):
          if result.success:
            return result.content

    return None
  
  def resolve(self, key):
    if key == "latest_summary":
      return self.get_previous_output()
    
    return None