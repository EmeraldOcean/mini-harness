from abc import *

class BaseTool(ABC):
  name = ""
  parameters = {}
  description = ""
  observation = ""
  inputs = {}

  @abstractmethod
  def run(self, *args, **kwargs):
    pass


  def prepare_args(self, args, contexts_manager):
    for arg, source in self.inputs.items():
      if arg not in args:
        args[arg] = contexts_manager.resolve(source)
    return args