# BEGIN
from typing_extensions import Literal, Any, Unpack
from haskellian import promise as P
from dslog import Logger
from q.api import ReadQueue, WriteQueue
from q.kv import QueueKV
from q.pipelines import local as loc, connect as raw_connect
AnyT: type = Any # type: ignore
# UNCOMMENT from MODULE import INPUT, OUTPUT, SPEC_VARIABLE
# UNCOMMENT from TYPES import Queues, Pipelines
from ._types import Queues, Pipelines # DELETE
INPUT = int # DELETE
OUTPUT = int # DELETE

def input_queue(
  input_path: str, *, protocol: Literal['sqlite', 'fs'] = 'sqlite'
) -> QueueKV[INPUT]:
  return QueueKV.at(INPUT, input_path, protocol=protocol)

def output_queue(
  output_path: str, *, protocol: Literal['sqlite', 'fs'] = 'sqlite'
) -> QueueKV[OUTPUT]:
  return QueueKV.at(OUTPUT, output_path, protocol=protocol)

SPEC_VARIABLE = ... # DELETE
def queues(
  path: str, *,
  protocol: Literal['sqlite', 'fs'] = 'sqlite',
) -> Queues:
  return loc.local_queues(path, SPEC_VARIABLE, protocol=protocol) # type: ignore

@P.run
async def connect(
  Qin: ReadQueue[INPUT],
  Qout: WriteQueue[OUTPUT],
  queues: Queues, *,
  logger = Logger.rich().prefix('[CONNECT]')
):
  await raw_connect(Qin, Qout, queues, input_task='INPUT_TASK', logger=logger) # type: ignore

def run_pipelines(queues: Queues, **pipelines: Unpack[Pipelines]):
  from multiprocessing import Process
  processes = {
    task: Process(target=pipelines[task], args=queues[task])
    for task in queues.keys()
  }
  for process in processes.values():
    process.start()
  for process in processes.values():
    process.join()

def run(
  Qin: ReadQueue[INPUT],
  Qout: WriteQueue[OUTPUT],
  queues: Queues, **pipelines: Unpack[Pipelines]
):
  from multiprocessing import Process
  p = Process(target=connect, args=(Qin, Qout, queues))
  p.start()
  run_pipelines(queues, **pipelines)
  p.join()

__all__ = ['input_queue', 'output_queue', 'queues', 'connect', 'run_pipelines', 'run']

# END
from templang import parse
from q.pipelines import Tasks

def local(tasks: Tasks, module: str, types_module: str, spec_variable: str) -> str:
  translations = {
    'MODULE': module,
    'TYPES': types_module,
    'INPUT_TASK': tasks.input_task,
    'INPUT': tasks.Input.__name__,
    'OUTPUT': tasks.Output.__name__,
    'SPEC_VARIABLE': spec_variable
  }

  with open(__file__) as f:
    source = f.read()
  
  return parse(source, translations)
