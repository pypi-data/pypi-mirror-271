# BEGIN
from typing import Literal, TypedDict, Union, overload, TypeAlias
from q.api import ReadQueue, WriteQueue
from q.pipelines import TaskQueues, Pipeline
# UNCOMMENT from MODULE import MOD_IMPORTS

INPUT = int # DELETE
OUTPUT_TYPE = int # DELETE

# LOOP TASK INPUT OUTPUT_ID OUTPUT_TYPE
class TASK:
  In = INPUT
  Out = Union[
    # LOOP OUTPUT_ID OUTPUT_TYPE
    tuple[Literal['OUTPUT_ID'], OUTPUT_TYPE],
    # END
  ] # type: ignore
  QueueIn = ReadQueue[In]
  QueueOut = WriteQueue[Out]
  Queues = TaskQueues[In, Out]

  # LOOP OUTPUT_ID OUTPUT_TYPE
  @classmethod
  @overload
  def next(cls, task: Literal['OUTPUT_ID'], data: OUTPUT_TYPE) -> 'TASK.Out': ... # type: ignore
  # END
  @classmethod
  def next(cls, task, data):
    return task, data

# END
class Queues(TypedDict):
  # LOOP TASK TSKID
  TSKID: TaskQueues[TASK.In, TASK.Out]
  # END 

class Pipelines(TypedDict):
  # LOOP TASK TSKID
  TSKID: Pipeline[TASK.In, TASK.Out]
  # END

T_INP = T_OUT = int # DELETE
QueueIn: TypeAlias = ReadQueue[T_INP]
QueueOut: TypeAlias = WriteQueue[T_OUT]

__all__ = [
  # LOOP TASK
  'TASK',
  # END
  'Queues', 'Pipelines', 'QueueIn', 'QueueOut',
]
# END
from templang import parse
from ..specs import Tasks

def types(tasks: Tasks, module: str) -> str:
  with open(__file__) as f:
    source = f.read()

  imports = ', '.join(set(tasks.InType(id).__name__ for id in tasks.tasks.keys()))

  translations = {
    'MODULE': module, 'MOD_IMPORTS': imports + ', ' + tasks.Output.__name__,
    'T_INP': tasks.Input.__name__, 'T_OUT': tasks.Output.__name__,
    'TASK': [], 'TSKID': [], 'INPUT': [], 'OUTPUT_ID': [], 'OUTPUT_TYPE': [],
  }

  for id, task in tasks.tasks.items():
    translations['TASK'].append(id.title())
    translations['TSKID'].append(id)
    translations['INPUT'].append(task.Input.__name__)

    ids = []
    types = []
    for outId in task.outputs:
      out_type = tasks.InType(outId).__name__
      ids.append(outId)
      types.append(out_type)

    translations['OUTPUT_ID'].append(ids)
    translations['OUTPUT_TYPE'].append(types)

  return parse(source, translations)