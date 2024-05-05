# Queue Pipelines

> Declarative orchestration of asynchronous queue-based tasks

## Usage

### 1. State-machine specification

```python
from q.pipelines import Tasks, Task

# Input types for tasks
class Image:
  img: str

class Annotated(Image):
  annotation: str

# State machine declaration
# Task(INPUT_TYPES, *NEXT_TASK_IDs)
# Tasks({ taskID -> Task })
# 'output' is a special task ID
TASKS = Tasks(
  input_task='classify', Output=Result,
  tasks=(
    classify=Task(Image, 'annotate_digit', 'annotate_word'),
    annotate_digit=Task(Image, 'output'),
    annotate_work=Task(Image, 'output'),
  )
)
```

### 2. Generate code

```python
def codegen():
  TASKS.codegen(__file__, 'TASKS')
  # generated/
  #   types.py
  #   local.py
  #   __init__.py
  TASKS.codegen_pipelines(__file__)
  # pipelines/
  #   _classify.py
  #   _annotate_digit.py
  #   _annotate_word.py
  #   __init__.py
```

### 3. Pipelines implementation

Generated code:

```python
# pipelines/_classify.py
from ..generated import Classify

def classify(Qin: Classify.QueueIn, Qout: Classify.QueueOut):
  ...
```

E.g. implementation:

```python
# pipelines/_classify.py
from fastapi import FastAPI
import uvicorn
from ..generated import Classify

def classify(Qin: Classify.QueueIn, Qout: Classify.QueueOut):
  app = FastAPI()
  @app.get('/tasks')
  async def tasks():
    return await Qin.items()

  @app.post('/annotate')
  async def annotate(annotation: Literal['digit', 'word']):
    id, task = await Qin.read()
    if annotation == 'digit':
      next = Classify.next('digit', task)
    else:
      next = Classify.next('word', task)
    await Qout.push(id, next)
    await Qin.pop(id)

  uvicorn.run(app)
    
```

### 4. Run!

```python
from mypkg.pipelines import PIPELINES
from mypkg.generated import run, input_queue, output_queue, queues

def main(input_path: str, output_path: str, queues_path: str):
  Qin = input_queue(queues_path)
  Qout = output_queue(queues_path)
  Qs = queues(queues_path)
  run(Qin, Qout, Qs, **PIPELINES)
```

- Each of the pipelines runs on a separate process
- An extra "connect" process polls from all queues and dispatches to the appropriate next queues/output