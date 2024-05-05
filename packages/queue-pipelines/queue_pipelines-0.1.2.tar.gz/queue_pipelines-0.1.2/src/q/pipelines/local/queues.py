from typing import TypeVar, Any, Literal
import os
from q.kv import QueueKV
from ..specs import Task, Tasks
from ..types import TaskQueues, Queues

T = TypeVar('T')
Id = TypeVar('Id', bound=str)
Out = TypeVar('Out', bound=tuple)

def task_queues(
  path: str,
  task: Task[T, Id],
  OutputType: type[Out],
  protocol: Literal['sqlite', 'fs'] = 'sqlite',
):
  return TaskQueues(
    QueueKV.at(task.Input, os.path.join(path, 'in'), protocol=protocol),
    QueueKV.at(OutputType, os.path.join(path, 'out'), protocol=protocol),
  )

def local_queues(
  path: str, tasks: Tasks[T, Any, Id],
  *, protocol: Literal['sqlite', 'fs'] = 'sqlite',
) -> Queues[Id, T]:
  return {
    id: task_queues(
      path=os.path.join(path, id), task=task,
      OutputType=tasks.OutType(id),
      protocol=protocol
    )
    for id, task in tasks.tasks.items()
  }
