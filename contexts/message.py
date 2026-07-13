from dataclasses import dataclass

@dataclass
class Message:
  role: str
  content: object | None