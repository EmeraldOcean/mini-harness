from abc import *
from contexts import ToolResult
from concurrent.futures import ThreadPoolExecutor, TimeoutError

class BaseTool(ABC):
  name = ""
  parameters = {}
  description = ""
  observation = ""
  artifact_type = None
  inputs = {}
  retryable = False

  timeout = 10

  @abstractmethod
  def run(self, *args, **kwargs):
    pass


  def prepare_args(self, args, contexts_manager):
    for arg, source in self.inputs.items():
      if arg not in args:
        args[arg] = contexts_manager.get_artifact(source)
    return args
  

  def execute(self, *args, **kwargs):
    with ThreadPoolExecutor(max_workers=1) as executor:
      future = executor.submit(self.run, *args, **kwargs)
      try:
        return future.result(timeout=self.timeout)

      except TimeoutError as e:
        return ToolResult(
          name=self.name,
          parameters=kwargs,
          success=False,
          error=str(e),
          error_type="timeout",
          retryable=True
        )
          
      except Exception as e:
        return ToolResult(
          name=self.name,
          parameters=kwargs,
          success=False,
          error=str(e),
          error_type=type(e).__name__,
          retryable=False
        )