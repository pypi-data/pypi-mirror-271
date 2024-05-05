from typing import NamedTuple, Generic, TypeVar, Mapping, TypeAlias, Any, Callable
from q.api import Queue, ReadQueue, WriteQueue

A = TypeVar('A')
B = TypeVar('B')
Id = TypeVar('Id', bound=str)

class TaskQueues(NamedTuple, Generic[A, B]):
  inp: Queue[A]
  out: Queue[B]

In = TypeVar('In')
Out = TypeVar('Out')

Pipeline = Callable[[ReadQueue[A], WriteQueue[B]], None]
Pipelines: TypeAlias = Mapping[Id, Pipeline[A, A]]

Queues: TypeAlias = Mapping[Id, TaskQueues[A, tuple[Id, A]]]