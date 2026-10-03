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


  def get_artifact(self, artifact_type):
    for message in reversed(self.messages):
      if message.role == "tool":
        result = message.content

        if isinstance(result, ToolResult):
          if result.success and result.artifact_type == artifact_type:
            return result.content

    return None


  def has_successful_tool_call(self, name, parameters):
    for message in self.messages:
      if message.role != "tool":
        continue

      result = message.content

      if isinstance(result, ToolResult):
        if (result.name == name) and (result.parameters == parameters) and result.success:
          return True

    return False