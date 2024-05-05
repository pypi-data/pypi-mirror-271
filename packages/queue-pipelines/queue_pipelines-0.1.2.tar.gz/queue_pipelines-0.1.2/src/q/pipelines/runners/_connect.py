from typing import TypeVar
import asyncio
from haskellian import IsLeft
from dslog import Logger
from q.api import ReadQueue, WriteQueue
from ..specs import OutId
from ..types import Queues

Id = TypeVar('Id', bound=str)
A = TypeVar('A')
B = TypeVar('B')

def input_item(id: Id, item: A) -> tuple[Id, A]:
  return id, item

async def connect(
  Qin: ReadQueue[A],
  Qout: WriteQueue[B],
  queues: Queues[Id, A], *,
  input_task: Id,
  logger = Logger.rich().prefix('[CONNECT]')
):
  async def connect_output(name: str, Qw: ReadQueue[tuple[OutId[Id], A]]):
    while True:
      try:
        id, (next_id, next_inp) = (await Qw.read()).unsafe()
        logger(f'Next task from "{name}": "{id}" -> "{next_id}"')
        Qnext = Qout if next_id == 'output' else queues[next_id].inp
        (await Qnext.push(id, next_inp)).unsafe() # type: ignore (Output should be a subtype of outer, but good luck expressing that with TypeVars)
        (await Qw.pop(id)).unsafe()
        await asyncio.sleep(0) # release the loop
      except IsLeft as e:
        logger('Queues error', e, level='ERROR')
        await asyncio.sleep(1)
      except Exception as e:
        logger('Unexpected error', e, level='ERROR')
        await asyncio.sleep(1)
  
  tasks = (
    connect_output('input', Qin.map(lambda it: (input_task, it))), *[
    connect_output(name, Qw)
      for name, (_, Qw) in queues.items()
  ])
  logger('Starting...')
  await asyncio.gather(*tasks)