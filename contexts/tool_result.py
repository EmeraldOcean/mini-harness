from dataclasses import dataclass

@dataclass
class ToolResult:
  name: str
  parameters: dict
  success: bool
  content: str | None = None
  error: str | None = None
  observation: str | None = None