from abc import *

class BaseTool(ABC):
  @abstractmethod
  def run(self, *args, **kwargs):
    pass