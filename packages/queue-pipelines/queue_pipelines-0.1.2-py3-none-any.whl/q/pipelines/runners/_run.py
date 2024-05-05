from typing import TypeVar, Mapping
from multiprocessing import Process
from haskellian import promise as P
from dslog import Logger
from q.api import ReadQueue, WriteQueue
from ..types import Queues
from ._connect import connect

Id = TypeVar('Id', bound=str)
A = TypeVar('A')
B = TypeVar('B')

def run_pipelines(queues: Queues[Id, A], **pipelines) -> Mapping[str, Process]:
  return {
    task: Process(target=pipelines[task], args=queues[task])
    for task in queues.keys()
  }

def run(
  Qin: ReadQueue[A],
  Qout: WriteQueue[B],
  queues: Queues[Id, A], *,
  input_task: Id,
  connect_logger = Logger.rich().prefix('[RUN]'),
  **pipelines
) -> Mapping[str, Process]:
  """Returns a mapping of task names to unstarted processes"""
  p = Process(
    target=P.run(connect), args=(Qin, Qout, queues),
    kwargs=dict(input_task=input_task, logger=connect_logger)
  )
  return run_pipelines(queues, **pipelines) | dict(connect=p)
