from dataclasses import dataclass

@dataclass
class ToolResult:
  name: str
  parameters: dict
  success: bool
  content: str | None = None
  error: str | None = None
  observation: str | None = None
  artifact_type: str | None = None

  error_type: str | None = None
  retryable: bool = False