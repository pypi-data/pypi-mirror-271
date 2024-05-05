# BEGIN
# UNCOMMENT from MODULE import TASK
from ._types import TASK # DELETE

def TSKID(
  Qin: TASK.QueueIn, Qout: TASK.QueueOut,
):
  ...
# END
from typing import TypeVar, Mapping
from templang import parse
from ..specs import Tasks

A = TypeVar('A')
B = TypeVar('B')
Id = TypeVar('Id', bound=str)

def pipeline(source: str, taskId: str, types_module: str):
  translations = {
    'MODULE': types_module,
    'TASK': taskId.title(),
    'TSKID': taskId
  }

  return parse(source, translations)

def pipelines(tasks: Tasks[A, B, Id], types_module: str) -> Mapping[Id, str]:
  with open(__file__) as f:
    source = f.read()
  return {
    task: pipeline(source, task, types_module)
    for task in tasks.tasks.keys()
  }